function branches = poly_branches(coefficients, tObs, options)
%POLY_BRANCHES Branches of a polynomial time map t(tau) at one observation time.
%   Coefficients use the MATLAB polyval convention, highest degree first. The
%   worldline is x(tau) = x0 + velocity*tau. Generic slices only: an
%   observation time whose preimage touches a critical point of the time map
%   is refused, because branch counting is ill-posed there; the critical point
%   itself belongs to pf.poly_critical_points and the classifier.
arguments
    coefficients (1,:) double
    tObs (1,1) double
    options.x0 (1,1) double = 0
    options.velocity (1,1) double = 1
    options.imagTol (1,1) double = 1e-9
    options.residualTol (1,1) double = 1e-10
    options.derivativeFloor (1,1) double = 1e-9
end

shifted = coefficients;
shifted(end) = shifted(end) - tObs;
if numel(shifted) > 1
    candidates = roots(shifted);
else
    candidates = [];
end
tau = sort(real(candidates(abs(imag(candidates)) <= options.imagTol)));
tau = tau(:);
derivative = polyder(coefficients);
n = numel(tau);
orientation = zeros(n, 1);
for k = 1:n
    residual = abs(polyval(shifted, tau(k)));
    if residual > options.residualTol
        error('pf:poly_branches:Residual', ...
            'root residual %g exceeds %g', residual, options.residualTol);
    end
    slope = polyval(derivative, tau(k));
    if abs(slope) <= options.derivativeFloor
        error('pf:poly_branches:NonGenericSlice', ...
            ['non-generic slice: a preimage lies on a critical point; ' ...
             'use pf.poly_critical_points for the fold itself']);
    end
    orientation(k) = sign(slope);
end
x = options.x0 + options.velocity * tau;
branches = table(tau, repmat(tObs, n, 1), x, orientation, ...
    'VariableNames', {'tau', 't', 'x', 'orientation'});
end
