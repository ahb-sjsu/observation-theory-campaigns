function dydtau = toy_rhs(~, y, p)
%TOY_RHS Hamiltonian toy dynamics.
% State: [t; p_t; x; p_x; u; p_u].
t = y(1); pt = y(2); px = y(4); u = y(5); pu = y(6);
coupling = p.g * p.field;
forceT = -(p.omega_t^2)*t - coupling*u;
forceU = -(p.omega_u^2)*u - p.lambda*u^3 - coupling*t;
dydtau = [pt; forceT; px; 0; pu; forceU];
end
