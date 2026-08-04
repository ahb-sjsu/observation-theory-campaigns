%% PF-1 structural stability pilot
clear; close all;
rng(20260803,'twister');

nTrials = 500;
epsValues = logspace(-5,-0.5,12);
persistence = zeros(size(epsValues));
medianExponent = nan(size(epsValues));

for e = 1:numel(epsValues)
    epsilon = epsValues(e);
    survived = false(nTrials,1);
    exponents = nan(nTrials,1);
    for trial = 1:nTrials
        c3 = randn; c4 = randn;
        % t(tau)=tau^2 + eps*(c3*tau^3+c4*tau^4).
        derivativeCoefficients = [4*epsilon*c4, 3*epsilon*c3, 2, 0];
        critical = roots(derivativeCoefficients);
        critical = critical(abs(imag(critical))<1e-10);
        critical = real(critical(abs(real(critical))<0.25));
        if isempty(critical)
            continue;
        end
        [~,idx] = min(abs(critical));
        tau0 = critical(idx);
        second = 2 + 6*epsilon*c3*tau0 + 12*epsilon*c4*tau0^2;
        if abs(second) < 1e-4
            continue;
        end
        survived(trial) = true;

        t0 = tau0^2 + epsilon*(c3*tau0^3+c4*tau0^4);
        deltaT = logspace(-8,-3,40)';
        if second < 0
            deltaT = -deltaT;
        end
        sep = nan(size(deltaT));
        for j = 1:numel(deltaT)
            target = t0 + deltaT(j);
            poly = [epsilon*c4, epsilon*c3, 1, 0, -target];
            rr = roots(poly);
            rr = sort(real(rr(abs(imag(rr))<1e-7 & abs(real(rr)-tau0)<0.1)));
            if numel(rr)>=2
                sep(j) = rr(end)-rr(1);
            end
        end
        good = isfinite(sep) & sep>0;
        if nnz(good)>=8
            fit = polyfit(log(abs(deltaT(good))),log(sep(good)),1);
            exponents(trial)=fit(1);
        end
    end
    persistence(e)=mean(survived);
    medianExponent(e)=median(exponents,'omitnan');
end

figure('Name','PF-1 Structural Stability');
semilogx(epsValues,persistence,'o-','LineWidth',1.5);
xlabel('perturbation norm'); ylabel('simple-fold persistence'); grid on;

figure('Name','PF-1 Separation Exponent');
semilogx(epsValues,medianExponent,'o-','LineWidth',1.5);
yline(0.5,'--'); xlabel('perturbation norm');
ylabel('median fitted exponent'); grid on;

results = table(epsValues(:),persistence(:),medianExponent(:), ...
    'VariableNames',{'epsilon','persistence','median_exponent'});
disp(results);
