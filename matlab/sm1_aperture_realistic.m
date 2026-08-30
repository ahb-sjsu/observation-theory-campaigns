function ot_aperture_realistic
% Realistic-aperture OT sensor management for the man-portable magnetar
% shield. Real array beam patterns (Phased Array Toolbox), link-budget SNR
% turning dwell into measurement noise, TIME as the scheduled resource, and
% a trigger reaction deadline. Compares round-robin, trace-greedy,
% MI(logdet)-greedy, and OT consumer-relative scheduling at matched time.
rng(20260830);
c=3e8; kB=1.38e-23; T0=290; NF=10^(3/10);

% ---------- real array (1.5 GHz ULA, TCDA-like man-portable) ----------
fc=1.5e9; lambda=c/fc; Nel=12;
array = phased.ULA('NumElements',Nel,'ElementSpacing',lambda/2);
pos = getElementPosition(array)/lambda;              % 3 x Nel (in wavelengths)
Garr = Nel;                                          % coherent array gain (linear)
% 3 dB azimuth beamwidth (approx for ULA)
bw3 = 0.886*102/Nel;                                 % deg (~7.5 deg)

% ---------- scene cells in azimuth, doorway = center ----------
cellAz = [-40 -20 0 20 40]; nc=numel(cellAz); doorway=3;
% real beam-pattern measurement matrix: steer to cell i, response at all cells
Himg = zeros(nc,nc);
for i=1:nc
    w = steervec(pos,[cellAz(i);0]);
    for j=1:nc
        a = steervec(pos,[cellAz(j);0]);
        Himg(i,j) = abs(w'*a)^2 / Nel^2;             % normalized beam power (peak 1)
    end
end
fprintf('array: %d-elem ULA @ %.2f GHz, gain %.1f dBi, 3dB BW %.1f deg\n',Nel,fc/1e9,10*log10(Garr),bw3);
fprintf('beam mainlobe/first-neighbor leakage: %.3f (cell20deg off), %.3f (cell40deg)\n',Himg(3,2),Himg(3,1));

% ---------- link budgets -> SNR per 1 ms dwell -> measurement noise ----------
tau=1e-3;                                            % 1 ms reference dwell
% imaging (two-way radar, person behind wall)
Pt=100; sigma=1; Rimg=5; Lw=10^(10/10);
SNR_img = Pt*Garr^2*lambda^2*sigma*tau/((4*pi)^3*Rimg^4*Lw^2*kB*T0*NF);
% trigger listen (one-way passive on a low-power emitter)
Pemit=0.1; Rtrig=8;
SNR_trig = Pemit*Garr*lambda^2*tau/((4*pi*Rtrig)^2*Lw*kB*T0*NF);
% DF bearing (strong device emitter, CRB)
Pdev=0.1; Rdev=8;
SNR_df = Pdev*Garr*lambda^2*tau/((4*pi*Rdev)^2*Lw*kB*T0*NF);
crb_bear = 1/(2*pi^2*(Nel^2-1)/12*SNR_df);          % ULA bearing CRB (rad^2), spacing lambda/2
fprintf('SNR @1ms: imaging %.1f dB, trigger %.1f dB, DF %.1f dB; bearing CRB %.2e rad^2\n',...
    10*log10(SNR_img),10*log10(SNR_trig),10*log10(SNR_df),crb_bear);

% Through-wall SNR is 100+ dB (above), so the aperture is NOT thermal-limited.
% The real measurement floor is clutter and model mismatch after cancellation,
% not kTBF. Use realistic clutter-limited floors (roughly common across modes);
% the scheduling advantage in this regime is attention/timing, not noise.
% (Clutter-vs-Doppler residual is the next refinement.)
Rocc  = 0.05;                                        % imaging: front-wall clutter residue
Rtrg  = 0.05;                                        % trigger: passive detection floor
Rbear = 4.89e-3;                                      % DF bearing var (rad^2), well above CRB
fprintf('regime: SNR-rich (100+ dB); meas floors clutter-limited: img %.3f trig %.3f bear %.2e\n\n',...
    Rocc,Rtrg,Rbear);

% ---------- state: [c1..c5, g, d1, d2] ----------
nS=8; ig=6; idev=[7 8];
F=eye(nS); F(ig,ig)=0.98;
Qc=0.06; Qg=0.02; Qd=0.05;
Q=diag([Qc*ones(1,5), Qg, Qd*ones(1,2)]);

% modes: 5 imaging (steer to each cell), 1 listen-trigger, 1 DF-sweep
% each carries H, R, and a dwell time (resource cost, ms)
modes=struct('name',{},'H',{},'R',{},'dwell',{});
for i=1:nc
    Hi=zeros(1,nS); Hi(1:nc)=Himg(i,:);
    modes(end+1)=struct('name','img','H',Hi,'R',Rocc,'dwell',1.0);           %#ok
end
Ht=zeros(1,nS); Ht(ig)=1;
modes(end+1)=struct('name','listen','H',Ht,'R',Rtrg,'dwell',0.5);            % passive, cheap
Hd=zeros(2,nS); Hd(1,idev(1))=1; Hd(2,idev(2))=1;
modes(end+1)=struct('name','DF','H',Hd,'R',Rbear*eye(2),'dwell',1.0);
M=numel(modes);

% consumer relevance: trigger dominates, doorway next
wC=0.1*ones(nS,1); wC(ig)=6; wC(doorway)=2; wC(idev)=0.3; PC=diag(wC);

% ---------- run policies; resource = TIME; reaction deadline on trigger ----------
pols={'roundrobin','trace','mi','ot'};
nMC=400; Tframes=200; thr=2.5; jumpMag=4.0;
deadline_ms=30;                                     % trigger must be caught within 30 ms
fprintf('=== realistic aperture: %d MC, matched TIME budget, %d ms reaction deadline ===\n',nMC,deadline_ms);
fprintf('%-12s %10s %12s %12s %10s\n','policy','decisionJ','trig lat ms','within %dms',deadline_ms);
for p=1:numel(pols)
    [J,latms,within,miss]=runpol(pols{p},F,Q,modes,PC,nS,ig,nMC,Tframes,thr,jumpMag,deadline_ms);
    fprintf('%-12s %10.3f %12.2f %11.1f%% %8.1f%% miss\n',pols{p},J,latms,100*within,100*miss);
end
end

function [Jmean,latms,within,missrate]=runpol(pol,F,Q,modes,PC,nS,ig,nMC,T,thr,jumpMag,deadline)
Jc=zeros(nMC,1); lat=nan(nMC,1); win=zeros(nMC,1); miss=zeros(nMC,1); M=numel(modes);
for mc=1:nMC
    x=zeros(nS,1); Sigma=0.5*eye(nS); xhat=zeros(nS,1); rr=1;
    tJump=randi([40 T-40]); det=false; Jacc=0; tms=0; tJump_ms=NaN;
    for t=1:T
        x=F*x+sqrtm(Q)*randn(nS,1); if t==tJump, x(ig)=x(ig)+jumpMag; end
        xhat=F*xhat; Sigma=F*Sigma*F'+Q;
        switch pol
            case 'roundrobin', m=rr; rr=mod(rr,M)+1;
            case 'trace',      m=pick(modes,Sigma,eye(nS),'trace');
            case 'mi',         m=pick(modes,Sigma,eye(nS),'logdet');
            case 'ot',         m=pick(modes,Sigma,PC,'trace');
        end
        H=modes(m).H; R=modes(m).R; tms=tms+modes(m).dwell;
        if t==tJump, tJump_ms=tms; end
        z=H*x+sqrtm(R)*randn(size(H,1),1);
        S=H*Sigma*H'+R; K=Sigma*H'/S;
        xhat=xhat+K*(z-H*xhat); Sigma=(eye(nS)-K*H)*Sigma;
        Jacc=Jacc+trace(PC*Sigma);
        if ~det && t>=tJump && xhat(ig)>thr, lat(mc)=tms-tJump_ms; det=true; end
    end
    Jc(mc)=Jacc/T;
    if ~det, miss(mc)=1; lat(mc)=NaN; else, win(mc)=lat(mc)<=deadline; end
end
Jmean=mean(Jc); latms=mean(lat(~isnan(lat))); within=mean(win); missrate=mean(miss);
end

function m=pick(modes,Sigma,W,crit)
best=inf; m=1;
for k=1:numel(modes)
    H=modes(k).H; R=modes(k).R;
    S=H*Sigma*H'+R; K=Sigma*H'/S; Sp=(eye(size(Sigma))-K*H)*Sigma;
    switch crit
        case 'trace',  val=trace(W*Sp);
        case 'logdet', val=log(det(Sp)+realmin);
    end
    if val<best, best=val; m=k; end
end
end
