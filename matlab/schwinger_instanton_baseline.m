%% S0: circular worldline-instanton action baseline
clear; close all;

mass = 1.7;
chargeField = 0.45;
Rstar = mass/chargeField;
Sstar = pi*mass^2/chargeField;
R = linspace(0,2.2*Rstar,2000)';
S = 2*pi*mass*R - pi*chargeField*R.^2;

% The Euclidean instanton is an extremum; in this reduced expression it is
% the stationary radius. The physical tunnelling exponent uses Sstar.
[~,idx] = min(abs(R-Rstar));
fprintf('R*=%.12g, grid R=%.12g, S*=%.12g, grid S=%.12g\n', ...
    Rstar,R(idx),Sstar,S(idx));

% Verify stationary derivative and analytic action.
dSdR = 2*pi*mass - 2*pi*chargeField*Rstar;
assert(abs(dSdR) < 1e-12);
assert(abs(S(idx)-Sstar)/Sstar < 5e-3);

figure('Name','Schwinger Circular Action Baseline');
plot(R,S,'LineWidth',1.4); hold on;
xline(Rstar,'--'); yline(Sstar,'--');
xlabel('worldline radius R'); ylabel('S(R)'); grid on;
title('Circular worldline action: stationary point at m/|qE|');
