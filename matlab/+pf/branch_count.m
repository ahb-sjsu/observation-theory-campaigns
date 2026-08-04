function branches = branch_count(tObs, t0, tau0, a, x0, velocity)
%BRANCH_COUNT Exact branches of t=t0+a*(tau-tau0)^2 at tObs.
arguments
    tObs (1,1) double
    t0 (1,1) double = 0
    tau0 (1,1) double = 0
    a (1,1) double {mustBeNonzero} = 1
    x0 (1,1) double = 0
    velocity (1,1) double = 1
end

ratio = (tObs - t0) / a;
tol = 1e-12;
if ratio < -tol
    branches = table([], [], [], [], 'VariableNames', ...
        {'tau','t','x','orientation'});
    return;
end
if abs(ratio) <= tol
    branches = table(tau0, t0, x0, 0, 'VariableNames', ...
        {'tau','t','x','orientation'});
    return;
end

root = sqrt(ratio);
tau = [tau0-root; tau0+root];
dtdtau = 2*a*(tau-tau0);
orientation = sign(dtdtau);
x = x0 + velocity*(tau-tau0);
branches = table(tau, repmat(tObs,2,1), x, orientation, ...
    'VariableNames', {'tau','t','x','orientation'});
end

function mustBeNonzero(x)
if x == 0
    error('pf:branch_count:ZeroCoefficient', 'a must be nonzero.');
end
end
