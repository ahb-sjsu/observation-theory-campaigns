function ot_aperture_sched
% OT consumer-relative sensor management for the magnetar multifunction
% aperture. One measurement per frame (matched budget) across three
% scheduling policies. Metric: decision cost tr(P_C Sigma) and the
% safety-critical trigger-detection latency.
%
% State x = [c1 c2 c3 c4 ; g ; d1 d2]'
%   c1..c4 = scene-cell occupancy activity (c1 = doorway, decision-relevant)
%   g      = trigger/threat channel (rare jump = a command being sent)
%   d1 d2  = device bearings (DF)
rng(20260830);

nS   = 7;           % state dim
ig   = 5;           % index of trigger channel
idoor= 1;           % doorway cell index
idev = [6 7];       % device bearing indices

% dynamics: near-random-walk, trigger channel slightly more persistent
F = eye(nS); F(ig,ig) = 0.98;
Q = diag([0.05 0.05 0.05 0.05  0.02  0.08 0.08]);

% measurement modes (aperture allocations), one chosen per frame
% each mode: H (obs matrix), R (noise cov)
modes = struct('name',{},'H',{},'R',{});
for i=1:4
    modes(end+1) = struct('name',sprintf('image c%d',i),'H',ei(i,nS),'R',0.05); %#ok
end
modes(end+1) = struct('name','listen trigger','H',ei(ig,nS),'R',0.04);
modes(end+1) = struct('name','DF sweep','H',[ei(idev(1),nS);ei(idev(2),nS)],'R',0.10*eye(2));
M = numel(modes);

% consumer-relevance weighting P_C: trigger dominates, doorway next,
% peripheral cells and DF matter little to the entry decision
wC = 0.1*ones(nS,1);
wC(ig)    = 6.0;      % a trigger about to fire is catastrophic to miss
wC(idoor) = 2.0;      % doorway occupancy
wC(idev)  = 0.3;
PC = diag(wC);

policies = {'roundrobin','infogreedy','ot'};
nMC   = 300;          % Monte Carlo trials
T     = 120;          % frames per trial
thr   = 2.5;          % trigger-detection threshold on ghat
jumpMag = 4.0;        % trigger activation magnitude

results = struct();
for p = 1:numel(policies)
    pol = policies{p};
    Jcost = zeros(nMC,1);         % mean decision cost over run
    lat   = nan(nMC,1);           % trigger detection latency (frames)
    miss  = zeros(nMC,1);
    for mc = 1:nMC
        x = zeros(nS,1);
        Sigma = 0.5*eye(nS);
        xhat  = zeros(nS,1);
        rr = 1;                                   % round-robin pointer
        tJump = randi([30 T-30]);                 % when the trigger fires
        detected = false;
        Jacc = 0;
        for t = 1:T
            % --- truth propagate ---
            x = F*x + sqrtm(Q)*randn(nS,1);
            if t==tJump, x(ig) = x(ig)+jumpMag; end
            % --- KF predict ---
            xhat = F*xhat;
            Sigma = F*Sigma*F' + Q;
            % --- choose mode ---
            switch pol
                case 'roundrobin'
                    m = rr; rr = mod(rr,M)+1;
                case 'infogreedy'
                    m = pick(modes, Sigma, eye(nS));   % min tr(Sigma_post)
                case 'ot'
                    m = pick(modes, Sigma, PC);        % min tr(PC Sigma_post)
            end
            % --- measure + KF update ---
            H = modes(m).H; R = modes(m).R;
            z = H*x + sqrtm(R)*randn(size(H,1),1);
            S = H*Sigma*H' + R;
            K = Sigma*H'/S;
            xhat  = xhat + K*(z - H*xhat);
            Sigma = (eye(nS)-K*H)*Sigma;
            % --- costs / detection ---
            Jacc = Jacc + trace(PC*Sigma);
            if ~detected && t>=tJump && xhat(ig) > thr
                lat(mc) = t - tJump; detected = true;
            end
        end
        Jcost(mc) = Jacc / T;
        if ~detected, miss(mc) = 1; lat(mc) = NaN; end
    end
    results.(pol).Jcost = mean(Jcost);
    results.(pol).lat   = mean(lat(~isnan(lat)));
    results.(pol).latMed= median(lat(~isnan(lat)));
    results.(pol).miss  = mean(miss);
    results.(pol).detrate = 1-mean(miss);
end

fprintf('\n=== OT aperture sensor-management: %d MC x %d frames, matched 1 meas/frame ===\n',nMC,T);
fprintf('%-14s %12s %12s %12s %10s\n','policy','decisionJ','trig lat(mn)','trig lat(md)','det rate');
for p=1:numel(policies)
    r = results.(policies{p});
    fprintf('%-14s %12.3f %12.2f %12.1f %9.1f%%\n', policies{p}, r.Jcost, r.lat, r.latMed, 100*r.detrate);
end
% relative improvement of OT vs infogreedy
oi = results.ot; gi = results.infogreedy;
fprintf('\nOT vs info-greedy: decisionJ %.1f%% lower, trigger latency %.1f%% lower, det rate %+.1f pts\n',...
    100*(1-oi.Jcost/gi.Jcost), 100*(1-oi.lat/gi.lat), 100*(oi.detrate-gi.detrate));
end

function v = ei(i,n)
v = zeros(1,n); v(i)=1;
end

function m = pick(modes, Sigma, W)
% greedy: choose the mode minimizing tr(W * Sigma_post)
best = inf; m = 1;
for k=1:numel(modes)
    H=modes(k).H; R=modes(k).R;
    S=H*Sigma*H'+R; K=Sigma*H'/S; Sp=(eye(size(Sigma))-K*H)*Sigma;
    val = trace(W*Sp);
    if val<best, best=val; m=k; end
end
end
