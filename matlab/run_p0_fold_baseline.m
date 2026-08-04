%% PF-0 exact fold baseline
clear; close all;

observationTimes = [-1, 0, 0.25, 1.0];
for k = 1:numel(observationTimes)
    branches = pf.branch_count(observationTimes(k));
    fprintf('t=%g: branches=%d, signed=%d\n', observationTimes(k), ...
        height(branches), sum(branches.orientation));
    disp(branches);
end

% Worldline t=tau^2, x=tau.
tau = linspace(-2,2,2001)';
t = tau.^2;
x = tau;
figure('Name','PF-0 Exact Fold');
plot(x,t,'LineWidth',1.5);
xlabel('projected position x');
ylabel('coordinate time t');
title('A smooth hidden trajectory seen through a time fold');
grid on;

% Local square-root separation law.
tObs = logspace(-6,0,100)';
separation = 2*sqrt(tObs);
coefficients = polyfit(log(tObs),log(separation),1);
fprintf('Fitted separation exponent: %.12f (target 0.5)\n',coefficients(1));
assert(abs(coefficients(1)-0.5) < 1e-10);

% Degenerate critical point must not be classified as a fold.
assert(pf.classify_fold(0,0) == "degenerate");
assert(pf.classify_fold(0,2) == "creation-fold");
assert(pf.classify_fold(0,-2) == "annihilation-fold");
