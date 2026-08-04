function points = poly_critical_points(coefficients, options)
%POLY_CRITICAL_POINTS Locate and classify all real critical points of a
%   polynomial time map, using the same classifier as the dynamical pipeline.
%   A repeated root of the derivative (a degenerate critical point) is one
%   geometric point: root clusters within mergeTol collapse to their mean.
arguments
    coefficients (1,:) double
    options.firstTol (1,1) double = 1e-9
    options.secondTol (1,1) double = 1e-8
    options.imagTol (1,1) double = 1e-9
    options.mergeTol (1,1) double = 1e-8
end

d1 = polyder(coefficients);
d2 = polyder(d1);
if numel(d1) > 1
    candidates = roots(d1);
else
    candidates = [];
end
raw = sort(real(candidates(abs(imag(candidates)) <= options.imagTol)));
raw = raw(:);
tau = zeros(0, 1);
clusterStart = 1;
for k = 1:numel(raw)
    if k == numel(raw) || raw(k+1) - raw(k) > options.mergeTol
        tau(end+1, 1) = mean(raw(clusterStart:k)); %#ok<AGROW>
        clusterStart = k + 1;
    end
end
n = numel(tau);
t = zeros(n, 1);
firstDerivative = zeros(n, 1);
secondDerivative = zeros(n, 1);
classification = strings(n, 1);
for k = 1:n
    t(k) = polyval(coefficients, tau(k));
    firstDerivative(k) = polyval(d1, tau(k));
    secondDerivative(k) = polyval(d2, tau(k));
    classification(k) = pf.classify_fold(firstDerivative(k), ...
        secondDerivative(k), options.firstTol, options.secondTol);
end
points = table(tau, t, firstDerivative, secondDerivative, classification);
end
