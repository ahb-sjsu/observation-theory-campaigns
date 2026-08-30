function sm1_aperture_clutter(seed)
% Dynamic-clutter OT aperture scheduling. Through-wall imaging is
% clutter-limited: a MOVING occupant separates in Doppler (cheap, short
% dwell), a STILL occupant is buried in the clutter residue (expensive,
% needs long dwell), and platform motion raises the clutter floor. The
% scheduler must invest dwell to confirm a still doorway occupant while
% still catching the trigger within its reaction deadline.
%
% Modes: image-cell-i short (1 ms) or long (10 ms), listen-trigger, DF.
% Resource = TIME. Compares round-robin, trace-greedy, MI-greedy, OT.
if nargin<1, seed=20260830; end
rng(seed); fprintf('--- seed %d ---\n',seed);

nc=5; doorway=3; nS=8; ig=6; idev=[7 8];
F=eye(nS); F(ig,ig)=0.98;                       % occupancy persistent (F=1)
Q=diag([3e-4*ones(1,nc), 0.02, 0.05*ones(1,2)]); % near-static occupancy latent

% clutter-limited imaging noise: R = clutter * base / (motion_sep + dwell_gain)
Rmove0=0.05; Rstill0=0.6; dwellGain=0.9;
Rtrg=0.05; Rbear=5e-3;
% dwell (ms) per mode
tau_short=1; tau_long=10; tau_listen=0.5; tau_df=1;

% consumer relevance: doorway occupancy + trigger dominate
wC=0.1*ones(nS,1); wC(ig)=6; wC(doorway)=4; wC(idev)=0.3; PC=diag(wC);

pols={'roundrobin','trace','mi','ot'};
nMC=500; T=240; thr=2.5; jumpMag=4.0; deadline_ms=30;
occThr=0.5; occVarThr=0.08;   % confident-occupied gate

fprintf('=== dynamic-clutter aperture: %d MC, matched TIME, %d ms deadline ===\n',nMC,deadline_ms);
fprintf('still occupant needs long dwell in low clutter; platform motion raises clutter\n\n');
fprintf('%-12s %9s %11s %12s %13s %11s\n','policy','decJ','trig<30ms','trig miss','door-still det','door FA');
for p=1:numel(pols)
    r=runpol(pols{p},F,Q,PC,nc,doorway,nS,ig,idev,nMC,T,thr,jumpMag,deadline_ms,...
             Rmove0,Rstill0,dwellGain,Rtrg,Rbear,tau_short,tau_long,tau_listen,tau_df,occThr,occVarThr);
    fprintf('%-12s %9.3f %10.1f%% %10.1f%% %12.1f%% %10.1f%%\n',pols{p},...
        r.decJ,100*r.trigWithin,100*r.trigMiss,100*r.doorDet,100*r.doorFA);
end
end

function r=runpol(pol,F,Q,PC,nc,doorway,nS,ig,idev,nMC,T,thr,jumpMag,deadline,...
        Rmove0,Rstill0,dwellGain,Rtrg,Rbear,ts,tl,tlis,tdf,occThr,occVarThr)
decJ=zeros(nMC,1); trigW=zeros(nMC,1); trigMiss=zeros(nMC,1);
doorDet=nan(nMC,1); doorFA=nan(nMC,1);
for mc=1:nMC
    % ---- scene: motion type per cell (0 empty,1 moving,2 still) + occupancy ----
    mtype=randi([0 2],1,nc); occ=double(mtype>0);
    % doorway: 60% still-occupied (critical), else empty
    if rand<0.6, mtype(doorway)=2; occ(doorway)=1; else, mtype(doorway)=0; occ(doorway)=0; end
    doorTrueOcc = occ(doorway)>0;
    x=zeros(nS,1); x(1:nc)=occ(:);
    Sigma=0.5*eye(nS); xhat=zeros(nS,1);                 % prior: empty room (detect occupants)
    % ---- platform-motion clutter: 2-state (braced 1, moving 4) ----
    clutter=1; rr=1; tms=0; det=false; tJump=randi([60 T-60]); tJump_ms=NaN;
    Jacc=0; doorLatMs=NaN;
    modes = buildmodes(nc,nS,ig,idev,ts,tl,tlis,tdf);
    M=numel(modes);
    for t=1:T
        % platform motion switches occasionally
        if rand<0.03, clutter = (clutter==1)*4 + (clutter==4)*1; end
        x=F*x+sqrtm(Q)*randn(nS,1); if t==tJump, x(ig)=x(ig)+jumpMag; end
        xhat=F*xhat; Sigma=F*Sigma*F'+Q;
        % planning R (scheduler knows clutter via IMU, assumes worst-case still target)
        Rplan=@(k) planR(modes(k),clutter,Rstill0,dwellGain,Rtrg,Rbear,nc);
        switch pol
            case 'roundrobin', m=rr; rr=mod(rr,M)+1;
            case 'trace',      m=pickR(modes,Sigma,eye(nS),'trace',Rplan);
            case 'mi',         m=pickR(modes,Sigma,eye(nS),'logdet',Rplan);
            case 'ot',         m=pickR(modes,Sigma,PC,'trace',Rplan);
        end
        H=modes(m).H; tms=tms+modes(m).dwell;
        if t==tJump, tJump_ms=tms; end
        % actual R (true motion type of the imaged cell)
        Ract=trueR(modes(m),clutter,mtype,Rmove0,Rstill0,dwellGain,Rtrg,Rbear,nc);
        z=H*x+sqrtm(Ract)*randn(size(H,1),1);
        S=H*Sigma*H'+Ract; K=Sigma*H'/S;
        xhat=xhat+K*(z-H*xhat); Sigma=(eye(nS)-K*H)*Sigma;
        Jacc=Jacc+trace(PC*Sigma);
        if ~det && t>=tJump && xhat(ig)>thr, trigW(mc)=(tms-tJump_ms)<=deadline; det=true; end
        if isnan(doorLatMs) && xhat(doorway)>occThr && Sigma(doorway,doorway)<occVarThr
            doorLatMs=tms;   % first confident "occupied" call on doorway
        end
    end
    decJ(mc)=Jacc/T; if ~det, trigMiss(mc)=1; end
    calledOcc = ~isnan(doorLatMs);
    if doorTrueOcc, doorDet(mc)=calledOcc; else, doorFA(mc)=calledOcc; end
end
r.decJ=mean(decJ); r.trigWithin=mean(trigW); r.trigMiss=mean(trigMiss);
r.doorDet=mean(doorDet(~isnan(doorDet))); r.doorFA=mean(doorFA(~isnan(doorFA)));
end

function modes=buildmodes(nc,nS,ig,idev,ts,tl,tlis,tdf)
modes=struct('name',{},'H',{},'dwell',{},'cell',{});
for i=1:nc
    Hi=zeros(1,nS); Hi(i)=1;
    modes(end+1)=struct('name','imgS','H',Hi,'dwell',ts,'cell',i); %#ok
    modes(end+1)=struct('name','imgL','H',Hi,'dwell',tl,'cell',i); %#ok
end
Ht=zeros(1,nS); Ht(ig)=1; modes(end+1)=struct('name','listen','H',Ht,'dwell',tlis,'cell',0);
Hd=zeros(2,nS); Hd(1,idev(1))=1; Hd(2,idev(2))=1;
modes(end+1)=struct('name','DF','H',Hd,'dwell',tdf,'cell',0);
end

function R=planR(mode,clutter,Rstill0,dwellGain,Rtrg,Rbear,nc) %#ok
switch mode.name
    case {'imgS','imgL'}, R=clutter*Rstill0/(dwellGain*mode.dwell);  % worst-case still
    case 'listen',        R=Rtrg;
    case 'DF',            R=Rbear*eye(2);
end
end

function R=trueR(mode,clutter,mtype,Rmove0,Rstill0,dwellGain,Rtrg,Rbear,nc) %#ok
switch mode.name
    case {'imgS','imgL'}
        mt=mtype(mode.cell);
        if mt==2, R=clutter*Rstill0/(dwellGain*mode.dwell);   % still: clutter-limited
        else,     R=Rmove0/mode.dwell; end                    % moving/empty: Doppler-separated
    case 'listen', R=Rtrg;
    case 'DF',     R=Rbear*eye(2);
end
end

function m=pickR(modes,Sigma,W,crit,Rfun)
best=inf; m=1;
for k=1:numel(modes)
    H=modes(k).H; R=Rfun(k);
    S=H*Sigma*H'+R; K=Sigma*H'/S; Sp=(eye(size(Sigma))-K*H)*Sigma;
    switch crit
        case 'trace',  val=trace(W*Sp);
        case 'logdet', val=log(det(Sp)+realmin);
    end
    if val<best, best=val; m=k; end
end
end
