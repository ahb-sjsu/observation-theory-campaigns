%% PF-0 complete instrument net: N0, P0, P1, D0, M0
% Runs every kinematic control from the campaign table through the generic
% polynomial instrument and cross-checks it against the validated quadratic
% reference. run_p0_fold_baseline remains the P0 tangency check; this script
% covers the full net on generic slices. S0 lives in
% schwinger_instanton_baseline and E0 in run_p2_toy_hamiltonian.
clear; close all;

% N0 monotone time: one branch, orientation +1, no critical points, no folds.
for tObs = [-2, 0, 1.5]
    b = pf.poly_branches([1 0], tObs);
    assert(height(b) == 1 && b.orientation == 1 && abs(b.tau - tObs) < 1e-12);
end
assert(height(pf.poly_critical_points([1 0])) == 0);
fprintf('N0 monotone null: PASS\n');

% P0 creation fold t=tau^2 on generic slices, against pf.branch_count.
for tObs = [0.25, 1, 4]
    general = pf.poly_branches([1 0 0], tObs);
    reference = pf.branch_count(tObs);
    assert(height(general) == 2 && height(reference) == 2);
    assert(max(abs(sort(general.tau) - sort(reference.tau))) < 1e-12);
    assert(isequal(sort(general.orientation), sort(reference.orientation)));
    assert(sum(general.orientation) == 0);
end
fprintf('P0 quadratic cross-check vs branch_count: PASS\n');

% P1 annihilation fold t=-tau^2: two branches before, none after.
before = pf.poly_branches([-1 0 0], -1);
assert(height(before) == 2 && sum(before.orientation) == 0);
after = pf.poly_branches([-1 0 0], 1);
assert(height(after) == 0);
fprintf('P1 annihilation fold: PASS\n');

% D0 degenerate cubic t=tau^3: critical point must not read as a fold.
p = pf.poly_critical_points([1 0 0 0]);
assert(height(p) == 1 && p.classification(1) == "degenerate");
fprintf('D0 degenerate cubic: PASS\n');

% M0 double fold t=tau^3-tau: band structure 1-3-3-3-1, signed invariant +1,
% both critical points found at +/-1/sqrt(3) with correct orientation change.
coefficients = [1 0 -1 0];
foldTime = 2 / (3 * sqrt(3));
slices = [-1, -0.2, 0, 0.2, 1];
counts = zeros(size(slices));
for k = 1:numel(slices)
    b = pf.poly_branches(coefficients, slices(k));
    counts(k) = height(b);
    assert(sum(b.orientation) == 1);
    assert(max(abs(polyval(coefficients, b.tau) - slices(k))) < 1e-10);
    if slices(k) == 0.2
        fprintf('M0 branch tau at t=0.2: %s\n', mat2str(b.tau', 15));
    end
end
assert(isequal(counts, [1 3 3 3 1]));
p = pf.poly_critical_points(coefficients);
assert(height(p) == 2);
assert(p.classification(1) == "annihilation-fold");
assert(p.classification(2) == "creation-fold");
assert(abs(p.tau(1) + 1/sqrt(3)) < 1e-12 && abs(p.t(1) - foldTime) < 1e-12);
assert(abs(p.tau(2) - 1/sqrt(3)) < 1e-12 && abs(p.t(2) + foldTime) < 1e-12);
assert(max(abs(p.firstDerivative)) < 1e-12);
assert(min(abs(p.secondDerivative)) > 3.4);
fprintf('M0 double fold: PASS (band counts %s)\n', mat2str(counts));
disp(p);

% The instrument must refuse a slice through the fold point itself.
refused = false;
try
    pf.poly_branches([1 0 0], 0);
catch err
    refused = strcmp(err.identifier, 'pf:poly_branches:NonGenericSlice');
end
assert(refused);
fprintf('Non-generic slice refusal: PASS\n');

fprintf('INSTRUMENT NET COMPLETE: N0 P0 P1 D0 M0 all PASS\n');
