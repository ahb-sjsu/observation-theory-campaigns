function [value, isterminal, direction] = toy_events(~, y)
%TOY_EVENTS Locate zeros of dt/dtau=p_t without terminating integration.
value = y(2);
isterminal = 0;
direction = 0;
end
