%% PF-1 structural stability pilot
% Perturbs the exact fold with a full low-order polynomial deformation
%   t(tau) = tau^2 + eps*(c1*tau + c2*tau^2 + c3*tau^3 + c4*tau^4),
% with c_i ~ N(0,1). The constant term is omitted because it is a time
% translation absorbed by the slicing. Unlike a cubic/quartic-only
% deformation, the c1 term translates the fold and the c2 term attacks its
% nondegeneracy, so persistence is measured rather than forced. First-order
% perturbation theory predicts the fold location tau0 = -eps*c1/2 + O(eps^2)
% and curvature 2 + 2*eps*c2 + O(eps^2); both are checked quantitatively.
clear; close all;
rng(20260803,'twister');

nTrials = 500;
epsValues = logspace(-5,-0.5,12);
persistence = zeros(size(epsValues));
medianExponent = nan(size(epsValues));
medianShiftError = nan(size(epsValues));
medianCurvatureError = nan(size(epsValues));
lostCount = zeros(size(epsValues));
degenerateCount = zeros(size(epsValues));

for e = 1:numel(epsValues)
    epsilon = epsValues(e);
    survived = false(nTrials,1);
    exponents = nan(nTrials,1);
    shiftErrors = nan(nTrials,1);
    curvatureErrors = nan(nTrials,1);
    for trial = 1:nTrials
        c = randn(1,4);
        timePoly = [epsilon*c(4), epsilon*c(3), 1+epsilon*c(2), epsilon*c(1), 0];
        derivativePoly = polyder(timePoly);
        predicted = -epsilon*c(1)/2;
        critical = roots(derivativePoly);
        critical = real(critical(abs(imag(critical))<1e-10));
        critical = critical(abs(critical - predicted) < 0.25);
        if isempty(critical)
            lostCount(e) = lostCount(e) + 1;
            continue;
        end
        [~,idx] = min(abs(critical - predicted));
        tau0 = critical(idx);
        second = polyval(polyder(derivativePoly), tau0);
        if abs(second) < 1e-4
            degenerateCount(e) = degenerateCount(e) + 1;
            continue;
        end
        survived(trial) = true;
        shiftErrors(trial) = abs(tau0 - predicted);
        curvatureErrors(trial) = abs(second - (2 + 2*epsilon*c(2)));

        t0 = polyval(timePoly, tau0);
        deltaT = logspace(-8,-3,40)';
        if second < 0
            deltaT = -deltaT;
        end
        sep = nan(size(deltaT));
        for j = 1:numel(deltaT)
            shifted = timePoly;
            shifted(end) = shifted(end) - (t0 + deltaT(j));
            rr = roots(shifted);
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
    medianShiftError(e)=median(shiftErrors,'omitnan');
    medianCurvatureError(e)=median(curvatureErrors,'omitnan');
end

figure('Name','PF-1 Structural Stability');
semilogx(epsValues,persistence,'o-','LineWidth',1.5);
xlabel('perturbation norm'); ylabel('simple-fold persistence'); grid on;

figure('Name','PF-1 Separation Exponent');
semilogx(epsValues,medianExponent,'o-','LineWidth',1.5);
yline(0.5,'--'); xlabel('perturbation norm');
ylabel('median fitted exponent'); grid on;

figure('Name','PF-1 Perturbation Theory Check');
loglog(epsValues,medianShiftError,'o-','LineWidth',1.5); hold on;
loglog(epsValues,medianCurvatureError,'s-','LineWidth',1.5);
loglog(epsValues,epsValues.^2,'--');
legend('median |tau0 - (-eps c_1/2)|','median |t''''(tau0) - (2+2 eps c_2)|', ...
    'eps^2 reference','Location','northwest');
xlabel('perturbation norm'); ylabel('deviation from first order'); grid on;

results = table(epsValues(:),persistence(:),medianExponent(:), ...
    medianShiftError(:),medianCurvatureError(:),lostCount(:),degenerateCount(:), ...
    'VariableNames',{'epsilon','persistence','median_exponent', ...
    'median_shift_error','median_curvature_error','lost','degenerate'});
disp(results);
