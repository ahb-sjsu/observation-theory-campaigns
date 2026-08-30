function ot_aperture_sweep
% Robustness sweep for OT consumer-relative aperture scheduling.
% Vary kappa = (process noise of decision-IRRELEVANT states) / (trigger
% channel process noise), from 0.5 to 5. Add a mutual-information (log-det)
% baseline alongside trace-greedy, so the info baseline is not strawmanned.
% Question: is OT's advantage on decision cost + trigger latency robust
% across kappa, or an artifact of one tuning?
rng(20260830);

nS=7; ig=5; idoor=1; idev=[6 7];
kappas = [0.5 1 1.5 2 3 5];
nMC = 200; T=120; thr=2.5; jumpMag=4.0; Qg=0.02;

wC=0.1*ones(nS,1); wC(ig)=6; wC(idoor)=2; wC(idev)=0.3; PC=diag(wC);

pols = {'roundrobin','trace','mi','ot'};
fprintf('\n=== OT scheduling robustness sweep (%d MC, matched budget) ===\n',nMC);
fprintf('kappa = Q_irrelevant / Q_trigger\n\n');
fprintf('%6s | %-32s | %-32s\n','kappa','decision cost tr(PC Sigma)','trigger latency (frames)');
fprintf('%6s | %8s %8s %8s %8s | %8s %8s %8s %8s\n','',pols{:},pols{:});
for kap = kappas
    Qirr = kap*Qg;
    F=eye(nS); F(ig,ig)=0.98;
    Q=diag([Qirr Qirr Qirr Qirr  Qg  Qirr Qirr]);
    modes = buildmodes(nS,ig,idev);
    J=zeros(numel(pols),1); L=zeros(numel(pols),1);
    for pi=1:numel(pols)
        [J(pi),L(pi)] = runpol(pols{pi}, F,Q,modes,PC, nS,ig, nMC,T,thr,jumpMag);
    end
    fprintf('%6.1f | %8.3f %8.3f %8.3f %8.3f | %8.2f %8.2f %8.2f %8.2f\n',kap,J,L);
end
fprintf('\n(pols order: roundrobin, trace-greedy, MI/logdet-greedy, OT)\n');
end

function modes = buildmodes(nS,ig,idev)
modes = struct('name',{},'H',{},'R',{});
for i=1:4, modes(end+1)=struct('name','','H',ei(i,nS),'R',0.05); end %#ok
modes(end+1)=struct('name','','H',ei(ig,nS),'R',0.04);
modes(end+1)=struct('name','','H',[ei(idev(1),nS);ei(idev(2),nS)],'R',0.10*eye(2));
end

function [Jmean,Lmean] = runpol(pol, F,Q,modes,PC, nS,ig, nMC,T,thr,jumpMag)
Jc=zeros(nMC,1); lat=nan(nMC,1); M=numel(modes);
for mc=1:nMC
    x=zeros(nS,1); Sigma=0.5*eye(nS); xhat=zeros(nS,1); rr=1;
    tJump=randi([30 T-30]); det=false; Jacc=0;
    for t=1:T
        x=F*x+sqrtm(Q)*randn(nS,1); if t==tJump, x(ig)=x(ig)+jumpMag; end
        xhat=F*xhat; Sigma=F*Sigma*F'+Q;
        switch pol
            case 'roundrobin', m=rr; rr=mod(rr,M)+1;
            case 'trace',      m=pick(modes,Sigma,eye(nS),'trace');
            case 'mi',         m=pick(modes,Sigma,eye(nS),'logdet');
            case 'ot',         m=pick(modes,Sigma,PC,'trace');
        end
        H=modes(m).H; R=modes(m).R;
        z=H*x+sqrtm(R)*randn(size(H,1),1);
        S=H*Sigma*H'+R; K=Sigma*H'/S;
        xhat=xhat+K*(z-H*xhat); Sigma=(eye(nS)-K*H)*Sigma;
        Jacc=Jacc+trace(PC*Sigma);
        if ~det && t>=tJump && xhat(ig)>thr, lat(mc)=t-tJump; det=true; end
    end
    Jc(mc)=Jacc/T; if ~det, lat(mc)=T; end   % miss penalized as max latency
end
Jmean=mean(Jc); Lmean=mean(lat);
end

function m=pick(modes,Sigma,W,crit)
best=inf; m=1;
for k=1:numel(modes)
    H=modes(k).H; R=modes(k).R;
    S=H*Sigma*H'+R; K=Sigma*H'/S; Sp=(eye(size(Sigma))-K*H)*Sigma;
    switch crit
        case 'trace',  val=trace(W*Sp);
        case 'logdet', val=log(det(Sp)+realmin);   % MI-greedy: min posterior log-det
    end
    if val<best, best=val; m=k; end
end
end

function v=ei(i,n), v=zeros(1,n); v(i)=1; end
