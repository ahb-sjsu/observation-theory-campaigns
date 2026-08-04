function [branches, weights, entropyBits] = fiber_entropy(coefficients, tObs)
%FIBER_ENTROPY Pushforward branch weights and Shannon entropy at one slice.
%   For a hidden state uniform in tau, the coarea formula assigns each
%   preimage of the observed value a weight proportional to 1/|dt/dtau|,
%   normalized over the fiber. The entropy is observational coarse-grained
%   structure, not thermodynamic entropy production. Generic slices only;
%   delegates preimage location to pf.poly_branches.
arguments
    coefficients (1,:) double
    tObs (1,1) double
end

branches = pf.poly_branches(coefficients, tObs);
if height(branches) == 0
    weights = zeros(0, 1);
    entropyBits = 0;
    return;
end
derivative = polyder(coefficients);
raw = 1 ./ abs(polyval(derivative, branches.tau));
weights = raw / sum(raw);
entropyBits = -sum(weights .* log2(weights));
end
