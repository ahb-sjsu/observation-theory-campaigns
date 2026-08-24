% XPROTO-CSI shakedown on a REAL Doppler-fading channel (MATLAB
% Communications Toolbox comm.RayleighChannel -- proper Jakes fading).
% Certificate = CQI (SNR report) -> MCS; witness = HARQ ACK/NACK;
% false-clear = BLER under CSI aging. Three policies over the SAME real
% fading trace: naive (raw CQI), olla (HARQ-witnessed offset), fresh
% (per-TTI CQI = no aging control). Writes CSIREP-family.json.
%
% SUBSTRATE HONESTY: real Jakes Doppler fading + link-level BLER model +
% adaptive modulation/coding + HARQ. NOT 3GPP 5G NR (5G Toolbox is not
% licensed here) -- it is the PHY mechanism behind CQI aging, one step
% more real than the Python AR(1) sim, one step less than an NR RFsim.

seeds        = [0 1 2];
fd           = 200;        % Hz Doppler (high mobility) -- the aging regime
Ttti         = 1e-3;       % s
Ntti         = 6000;
reportPeriod = 20;         % TTIs between CQI reports
meanSNR      = 12;         % dB
targetBLER   = 0.10;
W            = 1.0;        % CQI noise / BLER-curve width (dB)
mcsReq       = linspace(-2, 22, 12);   % per-MCS SNR (dB) at targetBLER
ollaUp       = 0.1;
ollaDown     = ollaUp * (1 - targetBLER) / targetBLER;   % equilibrium=target

cells = {};
for si = 1:numel(seeds)
    seed = seeds(si);
    os = 4;                                  % oversample: fd <= SampleRate/10
    ch = comm.RayleighChannel('SampleRate', os/Ttti, ...
        'MaximumDopplerShift', fd, 'PathDelays', 0, 'AveragePathGains', 0, ...
        'NormalizePathGains', true, ...
        'RandomStream', 'mt19937ar with seed', 'Seed', seed);
    hfull = ch(ones(Ntti*os, 1));            % real Jakes fading, oversampled
    h   = hfull(1:os:end);                   % one gain per TTI
    snr = meanSNR + 20*log10(abs(h) + 1e-12);  % instantaneous SNR (dB)

    val = struct('naive', 0, 'olla', 0, 'fresh', 0);
    cqiErr = 0; mcsVar = 0;
    policies = ["naive", "olla", "fresh"];
    for pi = 1:numel(policies)
        p = policies(pi);
        rng(seed*10 + pi);                   % reproducible noise per policy
        est = snr(1); offset = 0; nack = 0; seen = zeros(1, numel(mcsReq)); errs = 0;
        for n = 1:Ntti
            if p == "fresh" || mod(n-1, reportPeriod) == 0
                est = snr(n) + W*randn;       % CQI = measured SNR + noise
            end
            eff = est; if p == "olla", eff = est + offset; end
            m = find(mcsReq <= eff, 1, 'last'); if isempty(m), m = 1; end
            seen(m) = 1;
            bler = 0.5*erfc((snr(n) - (mcsReq(m) - 1.28)) / (sqrt(2)*W));  % ~target at reqSNR
            isNack = rand < bler;             % HARQ on the AGED channel
            errs = errs + abs(snr(n) - est);
            if isNack, nack = nack + 1; end
            if p == "olla"
                if isNack, offset = offset - ollaDown; else, offset = offset + ollaUp; end
            end
        end
        val.(p) = nack / Ntti;
        if p == "naive", cqiErr = errs / Ntti; mcsVar = sum(seen); end
    end

    cells{end+1} = struct('seed', seed, 'mode', 'matlab_fading', 'fd_hz', fd, ...
        'report_period', reportPeriod, 'naive_bler', round(val.naive, 4), ...
        'olla_bler', round(val.olla, 4), 'fresh_bler', round(val.fresh, 4), ...
        'cqi_err_db', round(cqiErr, 3), 'n_tti', Ntti, 'mcs_var', mcsVar, ...
        'target_bler', targetBLER); %#ok<SAGROW>
    fprintf('seed %d: naive=%.4f olla=%.4f fresh=%.4f cqi_err=%.2fdB mcs_var=%d\n', ...
        seed, val.naive, val.olla, val.fresh, cqiErr, mcsVar);
end

rec = struct('family', 'F-CSI', 'mode', 'matlab_fading', ...
    'sim_is_code_validation_not_evidence', false, ...
    'constants', struct('fd_hz', fd, 'report_period', reportPeriod, ...
        'target_bler', targetBLER, 'mean_snr_db', meanSNR, 'duration_tti', Ntti, ...
        'substrate', ['MATLAB Communications Toolbox comm.RayleighChannel ' ...
        '(real Jakes Doppler fading); link-level BLER + AMC + HARQ; ' ...
        'NOT 3GPP 5G NR -- 5G Toolbox not licensed']), ...
    'cells', {cells});
fid = fopen('CSIREP-family.json', 'w');
fwrite(fid, jsonencode(rec, 'PrettyPrint', true));
fclose(fid);
fprintf('wrote CSIREP-family.json\n');
