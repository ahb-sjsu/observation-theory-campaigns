%% PF-2 local Hamiltonian negative control
clear; close all;

p = struct('omega_t',1.0,'omega_u',1.2,'lambda',0.1,'g',0.25,'field',1.0);
y0 = [0;1;0;0.2;0.1;0];
opts = odeset('RelTol',1e-10,'AbsTol',1e-12,'Events',@pf.toy_events,'MaxStep',0.01);
[tau,y,te,ye] = ode45(@(tau,y) pf.toy_rhs(tau,y,p),[0 40],y0,opts);
H = pf.toy_energy(y,p);
relativeDrift = max(abs(H-H(1)))/max(abs(H(1)),1);
fprintf('folds=%d, max relative energy drift=%.3e\n',numel(te),relativeDrift);

figure('Name','PF-2 Projected Worldline');
plot(y(:,3),y(:,1),'LineWidth',1.2); hold on;
if ~isempty(ye)
    scatter(ye(:,3),ye(:,1),35,'filled');
end
xlabel('x'); ylabel('coordinate time t'); grid on;
title('Toy Hamiltonian projection folds');

figure('Name','PF-2 Time Orientation');
plot(tau,y(:,2),'LineWidth',1.2); hold on; yline(0,'--');
xlabel('hidden evolution parameter \tau'); ylabel('dt/d\tau = p_t'); grid on;

figure('Name','PF-2 Energy Audit');
plot(tau,H-H(1),'LineWidth',1.2);
xlabel('\tau'); ylabel('H(\tau)-H(0)'); grid on;
