function sm2_aperture_qram(seed)
% SM-2: OT-DERIVED consumer-relative value vs HAND-TUNED fixed-priority
% (Q-RAM-style) revisit scheduling, at matched TIME budget, on the
% dynamic-clutter aperture. Q-RAM hand-sets task priorities/revisit
% intervals; OT derives a state-dependent value tr(P_C dSigma)/dwell from
% the consumer geometry. Claim: no single fixed tuning meets both the
% trigger deadline and still-occupant detection across the scene ensemble;
% OT adapts and approaches a per-scenario oracle without foreknowledge.
if nargin<1, seed=20260830; end
rng(seed); fprintf('--- seed %d ---\n',seed);

nc=5; doorway=3; nS=8; ig=6; idev=[7 8];
tick=0.5; budgetTicks=800; deadlineTicks=60;   % 0.5 ms tick, 400 ms budget, 30 ms deadline
Ft=eye(nS); Ft(ig,ig)=0.999;                    % per-tick dynamics
Qt=diag([1e-4*ones(1,nc), 8e-4, 2e-3*ones(1,2)]);
Rmove0=0.05; Rstill0=0.6; dwellGain=0.9; Rtrg=0.05; Rbear=5e-3;
thr=2.5; jumpMag=4.0; occThr=0.5; occVarThr=0.08;
wC=0.1*ones(nS,1); wC(ig)=6; wC(doorway)=4; wC(idev)=0.3; PC=diag(wC);

% modes: for i=1..5 push imgS(2i-1) imgL(2i); listen(11); DF(12)
modes=buildmodes(nc,nS,ig,idev,tick);
LISTEN=11; DF=12; imgL=@(c)2*c; imgS=@(c)2*c-1;

% Q-RAM fixed tunings for DISPLAY (3 representative), plus a GRID for a fair oracle
tunings=struct('name',{'trig-heavy','balanced','img-heavy'},...
    'rev',{[6 60 40 80],[20 40 40 60],[50 24 30 80]});
% fair oracle = best-per-scenario over a grid of fixed tunings (trigger x doorway rev)
grid=[]; for tr=[6 12 20 30 50], for dr=[24 40 60], grid=[grid; tr dr 40 70]; end; end
nGrid=size(grid,1);

policies={'OT','QRAM:trig-heavy','QRAM:balanced','QRAM:img-heavy','QRAM:oracle(grid)'};
nMC=400;
JS=zeros(numel(policies),1); TR=zeros(numel(policies),1); DR=zeros(numel(policies),1);
for mc=1:nMC
    % ---- scene ----
    mtype=randi([0 2],1,nc); occ=double(mtype>0);
    if rand<0.6, mtype(doorway)=2; occ(doorway)=1; else, mtype(doorway)=0; occ(doorway)=0; end
    doorTrueOcc=occ(doorway)>0;
    tJumpTick=randi([120 budgetTicks-120]);
    clutSeed=rand(1,budgetTicks); % shared clutter realization across policies (CRN)
    scene=struct('mtype',mtype,'occ',occ,'tJumpTick',tJumpTick,'clutSeed',clutSeed,...
        'doorTrueOcc',doorTrueOcc);
    measSeed=randn(nS+2,budgetTicks); % shared measurement-noise draws (CRN)
    % ---- OT ----
    [okT,okD]=simulate('OT',scene,modes,Ft,Qt,PC,nS,ig,doorway,idev,nc,...
        tick,budgetTicks,deadlineTicks,thr,jumpMag,occThr,occVarThr,...
        Rmove0,Rstill0,dwellGain,Rtrg,Rbear,[],measSeed,LISTEN,DF,imgL,imgS);
    JS(1)=JS(1)+(okT&&okD); TR(1)=TR(1)+okT; DR(1)=DR(1)+okD;
    % ---- QRAM display tunings (3 representative) ----
    for tI=1:numel(tunings)
        [okT,okD]=simulate('QRAM',scene,modes,Ft,Qt,PC,nS,ig,doorway,idev,nc,...
            tick,budgetTicks,deadlineTicks,thr,jumpMag,occThr,occVarThr,...
            Rmove0,Rstill0,dwellGain,Rtrg,Rbear,tunings(tI),measSeed,LISTEN,DF,imgL,imgS);
        JS(1+tI)=JS(1+tI)+(okT&&okD); TR(1+tI)=TR(1+tI)+okT; DR(1+tI)=DR(1+tI)+okD;
    end
    % ---- fair oracle: best-per-scenario over the fixed-tuning GRID ----
    oJoint=false; oT=false; oD=false;
    for g=1:nGrid
        [okT,okD]=simulate('QRAM',scene,modes,Ft,Qt,PC,nS,ig,doorway,idev,nc,...
            tick,budgetTicks,deadlineTicks,thr,jumpMag,occThr,occVarThr,...
            Rmove0,Rstill0,dwellGain,Rtrg,Rbear,struct('name','grid','rev',grid(g,:)),...
            measSeed,LISTEN,DF,imgL,imgS);
        if okT&&okD, oJoint=true; end; oT=oT||okT; oD=oD||okD;
    end
    JS(5)=JS(5)+oJoint; TR(5)=TR(5)+oT; DR(5)=DR(5)+oD;
end
JS=JS/nMC; TR=TR/nMC; DR=DR/nMC;
fprintf('\n=== SM-2: OT-derived vs hand-tuned Q-RAM, matched %d ms, %d MC ===\n',...
    budgetTicks*tick,nMC);
fprintf('%-20s %12s %14s %16s\n','policy','joint OK','trig<30ms','doorway correct');
for p=1:numel(policies)
    fprintf('%-20s %10.1f%% %12.1f%% %14.1f%%\n',policies{p},100*JS(p),100*TR(p),100*DR(p));
end
fprintf('\nOracle = best of the %d-point fixed-tuning GRID chosen per-scenario (hindsight).\n',nGrid);
fprintf('Scope: OT (derived, no per-task tuning) vs HAND-TUNED FIXED priorities.\n');
fprintf('Mechanism: fixed revisit cannot adapt WITHIN a trial (confirm occupant, then\n');
fprintf('guard trigger); OT does, from the consumer geometry alone. Not a claim over\n');
fprintf('adaptive/cognitive RRM, which would need an objective - which OT supplies.\n');
end

function [okTrig,okDoor]=simulate(pol,scene,modes,Ft,Qt,PC,nS,ig,doorway,idev,nc,...
    tick,budgetTicks,deadlineTicks,thr,jumpMag,occThr,occVarThr,...
    Rmove0,Rstill0,dwellGain,Rtrg,Rbear,tuning,measSeed,LISTEN,DF,imgL,imgS)
x=zeros(nS,1); x(1:nc)=scene.occ(:); Sigma=0.5*eye(nS); xhat=zeros(nS,1);
tk=0; det=false; okTrig=false; doorLat=NaN;
lastServ=zeros(1,4); cellRot=1;   % QRAM task timers, cell rotation
while tk<budgetTicks
    clutter = 1 + 3*(scene.clutSeed(min(tk+1,budgetTicks))<0.5); % 1 or 4 (shared CRN)
    % ---- choose mode ----
    if strcmp(pol,'OT')
        m=pickOT(modes,Sigma,PC,clutter,Rstill0,dwellGain,Rtrg,Rbear);
    else
        [m,cellRot]=pickQRAM(tuning,lastServ,tk,doorway,cellRot,nc,LISTEN,DF,imgL,imgS);
    end
    nt=modes(m).nt; H=modes(m).H;
    % ---- evolve truth + KF predict over the dwell ----
    for s=1:nt
        x=Ft*x+sqrtm(Qt)*measSeed(1:nS,min(tk+1,budgetTicks));
        if (tk+1)==scene.tJumpTick, x(ig)=x(ig)+jumpMag; end
        xhat=Ft*xhat; Sigma=Ft*Sigma*Ft'+Qt;
        tk=tk+1; if tk>=budgetTicks, break; end
    end
    % ---- measure (R from true motion type + dwell + clutter) ----
    Ract=trueR(modes(m),clutter,scene.mtype,Rmove0,Rstill0,dwellGain,Rtrg,Rbear);
    nz=size(H,1);
    z=H*x+sqrtm(Ract)*measSeed(nS+1:nS+nz,min(tk,budgetTicks));
    S=H*Sigma*H'+Ract; K=Sigma*H'/S;
    xhat=xhat+K*(z-H*xhat); Sigma=(eye(nS)-K*H)*Sigma;
    % update QRAM timers
    if ~strcmp(pol,'OT'), lastServ=updTimers(lastServ,m,tk,doorway,LISTEN,DF,imgL); end
    % ---- outcomes ----
    if ~det && tk>=scene.tJumpTick && xhat(ig)>thr
        okTrig=(tk-scene.tJumpTick)<=deadlineTicks; det=true;
    end
    if isnan(doorLat) && xhat(doorway)>occThr && Sigma(doorway,doorway)<occVarThr
        doorLat=tk;
    end
end
calledOcc=~isnan(doorLat);
okDoor = (scene.doorTrueOcc && calledOcc) || (~scene.doorTrueOcc && ~calledOcc);
end

function modes=buildmodes(nc,nS,ig,idev,tick)
modes=struct('name',{},'H',{},'dwell',{},'cell',{},'nt',{});
for i=1:nc
    Hi=zeros(1,nS); Hi(i)=1;
    modes(end+1)=struct('name','imgS','H',Hi,'dwell',1,'cell',i,'nt',round(1/tick));   %#ok
    modes(end+1)=struct('name','imgL','H',Hi,'dwell',10,'cell',i,'nt',round(10/tick)); %#ok
end
Ht=zeros(1,nS); Ht(ig)=1; modes(end+1)=struct('name','listen','H',Ht,'dwell',0.5,'cell',0,'nt',1);
Hd=zeros(2,nS); Hd(1,idev(1))=1; Hd(2,idev(2))=1;
modes(end+1)=struct('name','DF','H',Hd,'dwell',1,'cell',0,'nt',round(1/tick));
end

function m=pickOT(modes,Sigma,PC,clutter,Rstill0,dwellGain,Rtrg,Rbear)
best=-inf; m=1; base=trace(PC*Sigma);
for k=1:numel(modes)
    H=modes(k).H; R=planR(modes(k),clutter,Rstill0,dwellGain,Rtrg,Rbear);
    S=H*Sigma*H'+R; K=Sigma*H'/S; Sp=(eye(size(Sigma))-K*H)*Sigma;
    val=(base-trace(PC*Sp))/modes(k).dwell;   % consumer-relevant reduction PER TIME
    if val>best, best=val; m=k; end
end
end

function [m,cellRot]=pickQRAM(tuning,lastServ,tk,doorway,cellRot,nc,LISTEN,DF,imgL,imgS)
% urgency = ticks_since_service / revisit_interval; serve most urgent task
urg=(tk-lastServ)./tuning.rev;
[~,task]=max(urg);
switch task
    case 1, m=LISTEN;
    case 2, m=imgL(doorway);                    % doorway: long dwell to catch still
    case 3                                       % rotate non-doorway cells, short dwell
        c=cellRot; if c==doorway, c=mod(c,nc)+1; end
        m=imgS(c); cellRot=mod(c,nc)+1;
    case 4, m=DF;
end
end

function lastServ=updTimers(lastServ,m,tk,doorway,LISTEN,DF,imgL)
if m==LISTEN, lastServ(1)=tk;
elseif m==imgL(doorway), lastServ(2)=tk;
elseif m==DF, lastServ(4)=tk;
else, lastServ(3)=tk; end
end

function R=planR(mode,clutter,Rstill0,dwellGain,Rtrg,Rbear)
switch mode.name
    case {'imgS','imgL'}, R=clutter*Rstill0/(dwellGain*mode.dwell);
    case 'listen', R=Rtrg;
    case 'DF', R=Rbear*eye(2);
end
end
function R=trueR(mode,clutter,mtype,Rmove0,Rstill0,dwellGain,Rtrg,Rbear)
switch mode.name
    case {'imgS','imgL'}
        if mtype(mode.cell)==2, R=clutter*Rstill0/(dwellGain*mode.dwell);
        else, R=Rmove0/mode.dwell; end
    case 'listen', R=Rtrg;
    case 'DF', R=Rbear*eye(2);
end
end
