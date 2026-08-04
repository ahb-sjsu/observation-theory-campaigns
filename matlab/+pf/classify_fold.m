function label = classify_fold(firstDerivative, secondDerivative, firstTol, secondTol)
%CLASSIFY_FOLD Classify a scalar time critical point.
arguments
    firstDerivative (1,1) double
    secondDerivative (1,1) double
    firstTol (1,1) double = 1e-9
    secondTol (1,1) double = 1e-8
end
if abs(firstDerivative) > firstTol
    label = "regular";
elseif abs(secondDerivative) <= secondTol
    label = "degenerate";
elseif secondDerivative > 0
    label = "creation-fold";
else
    label = "annihilation-fold";
end
end
