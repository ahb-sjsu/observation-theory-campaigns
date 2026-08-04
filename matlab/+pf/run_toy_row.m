function result = run_toy_row(row)
%RUN_TOY_ROW Execute one manifest row and return a scalar structure.
p = struct( ...
    'omega_t', row.omega_t, ...
    'omega_u', row.omega_u, ...
    'lambda', row.lambda, ...
    'g', row.g, ...
    'field', row.field);
y0 = [row.t0; row.pt0; row.x0; row.px0; row.u0; row.pu0];
opts = odeset('RelTol',1e-10,'AbsTol',1e-12,'Events',@pf.toy_events, ...
    'MaxStep', max(row.dt, 1e-4));
[tau,y,te,ye] = ode45(@(tau,y) pf.toy_rhs(tau,y,p), [0 row.tau_max], y0, opts);
H = pf.toy_energy(y,p);
scale = max(abs(H(1)),1);
result = struct();
result.scenario_id = string(row.scenario_id);
result.fold_count = numel(te);
result.fold_tau = te(:)';
result.fold_t = ye(:,1)';
result.fold_x = ye(:,3)';
result.fold_accel_t = arrayfun(@(k) pf.toy_rhs(te(k),ye(k,:)',p),1:numel(te), ...
    'UniformOutput',false);
if isempty(result.fold_accel_t)
    result.fold_accel_t = [];
else
    result.fold_accel_t = cellfun(@(v) v(2), result.fold_accel_t);
end
result.energy_initial = H(1);
result.energy_final = H(end);
result.max_relative_energy_drift = max(abs(H-H(1)))/scale;
result.n_points = numel(tau);
result.final_state = y(end,:);
end
