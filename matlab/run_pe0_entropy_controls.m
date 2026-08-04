%% PE-0 analytic entropy controls (plus the PE-1 convergence slice)
% Pushforward branch weights and conditional branch entropy across the
% kinematic control net, checked against closed-form values. The signed
% degree stays fixed while observational multiplicity and branch entropy
% change. Nothing here is thermodynamic entropy production; these are
% observational quantities of the projection.
clear; close all;

% P0 fold: two equal-weight branches, exactly one bit, signed count zero.
for tObs = [0.04, 0.25, 1]
    [b, w, h] = pf.fiber_entropy([1 0 0], tObs);
    assert(height(b) == 2 && sum(b.orientation) == 0);
    assert(max(abs(w - 0.5)) < 1e-12);
    assert(abs(h - 1) < 1e-12);
end
[~, ~, h] = pf.fiber_entropy([1 0 0], -1);
assert(h == 0);
fprintf('PE-0 P0 fold: exactly one bit, signed count 0: PASS\n');

% M0 symmetric slice: weights (1/4, 1/2, 1/4), entropy exactly 1.5 bits.
[b, w, h] = pf.fiber_entropy([1 0 -1 0], 0);
assert(height(b) == 3 && sum(b.orientation) == 1);
assert(max(abs(sort(w) - [0.25; 0.25; 0.5])) < 1e-10);
assert(abs(h - 1.5) < 1e-9);
fprintf('PE-0 M0 symmetric slice: exactly 1.5 bits, signed count +1: PASS\n');

% M0 band edge: the merging pair dominates the fiber measure, entropy -> 1 bit.
edgeT = 2 / (3 * sqrt(3));
[~, ~, h] = pf.fiber_entropy([1 0 -1 0], edgeT - 1e-9);
assert(abs(h - 1) < 1e-3);
fprintf('PE-0 M0 band edge: entropy -> 1 bit: PASS\n');

% N0 and D0: single branch everywhere, zero branch ambiguity. The degenerate
% critical point creates no ambiguity because t = tau^3 stays monotone.
for tObs = [-0.5, 0.5]
    [b1, ~, h1] = pf.fiber_entropy([1 0], tObs);
    [b2, ~, h2] = pf.fiber_entropy([1 0 0 0], tObs);
    assert(height(b1) == 1 && h1 == 0);
    assert(height(b2) == 1 && h2 == 0);
end
fprintf('PE-0 N0/D0: zero branch entropy: PASS\n');

% PE-1 slice: binned pushforward entropy of the exact fold converges to the
% differential limit 1 - 1/ln(2) bits after removing the log2(eps) term. The
% inverse-square-root caustic is integrable and produces no pathology.
limitBits = 1 - 1/log(2);
epsilons = [1e-4, 1e-5, 1e-6];
deviation = zeros(size(epsilons));
for k = 1:numel(epsilons)
    edges = 0:epsilons(k):1;
    masses = diff(sqrt(edges));
    masses = masses(masses > 0);
    H = -sum(masses .* log2(masses));
    deviation(k) = abs(H + log2(epsilons(k)) - limitBits);
end
assert(all(diff(deviation) < 0) && deviation(end) < 0.05);
fprintf('PE-1 binned entropy convergence: deviations %s: PASS\n', ...
    mat2str(deviation, 3));

fprintf('ENTROPY CONTROLS COMPLETE: PE-0 all PASS, PE-1 convergence PASS\n');
