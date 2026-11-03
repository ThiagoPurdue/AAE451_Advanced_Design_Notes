% sizing_loop.m
% Takeoff-weight sizing by iteration, AAE 451 Advanced Aircraft Design, Lecture 2.
%
% Empty weight and fuel weight are both functions of the takeoff weight W0,
% so W0 is found by iteration: guess W0, compute both, sum with crew and
% payload, compare with the guess, repeat.
%
% The inputs below describe a small jet transport with invented values, so
% that the example is not the Navy Jet Trainer. Your sizing code takes its
% mission from your RFP and its sizing variables from your constraint
% analysis.

clear; clc;

% --- Fixed weights, lb (example values) ---
W_crew    = 600;      % three crew with equipment
W_payload = 8000;     % 40 passengers with bags, 200 lb each

% --- Design mission (example values) ---
R_cruise  = 1500 * 6076;    % cruise range, ft (1,500 nmi)
V_cruise  = 450 * 1.688;    % cruise true airspeed, ft/s (450 kt)
C_cruise  = 0.60 / 3600;    % thrust specific fuel consumption in cruise, 1/s
LD_cruise = 15;             % lift-to-drag ratio in cruise
E_loiter  = 20 * 60;        % loiter endurance, s (20 min)
C_loiter  = 0.60 / 3600;    % thrust specific fuel consumption in loiter, 1/s
LD_loiter = 16;             % lift-to-drag ratio in loiter
k         = 0.06;           % trapped fuel 1 percent plus 5 percent reserves

% --- Empty weight: bomber and transport trend line, Nicolai Table 5.1 ---
We_of_W0 = @(W0) 0.911 * W0.^0.947;

% --- Fuel weight: product of segment fractions ---
f_takeoff = 0.970;                                        % Raymer Table 3.2
f_climb   = 0.985;                                        % Raymer Table 3.2
f_cruise  = exp(-R_cruise * C_cruise / (V_cruise * LD_cruise));   % Breguet range
f_loiter  = exp(-E_loiter * C_loiter / LD_loiter);               % Breguet endurance
f_landing = 0.995;                                        % Raymer Table 3.2
Wfuel_frac = (1 + k) * (1 - f_takeoff * f_climb * f_cruise * f_loiter * f_landing);
Wfuel_of_W0 = @(W0) Wfuel_frac * W0;

% --- The sizing loop ---
W0_guess = 20000;          % lb, initial guess
tolerance = 1;             % lb
fprintf('Fuel weight fraction Wfuel/W0 = %.3f\n\n', Wfuel_frac);
fprintf('%5s %12s %12s %12s %12s\n', 'iter', 'W0 guess', 'We', 'Wfuel', 'W0 calc');
for iteration = 1:100
    We    = We_of_W0(W0_guess);
    Wfuel = Wfuel_of_W0(W0_guess);
    W0_calc = (W_crew + W_payload) / (1 - We / W0_guess - Wfuel / W0_guess);
    fprintf('%5d %12.0f %12.0f %12.0f %12.0f\n', iteration, W0_guess, We, Wfuel, W0_calc);
    if abs(W0_calc - W0_guess) < tolerance
        break
    end
    W0_guess = W0_calc;    % (W0)guess = (W0)calc, and back to the top
end

fprintf('\nConverged after %d iterations: W0 = %.0f lb (We/W0 = %.3f, Wfuel/W0 = %.3f)\n', ...
    iteration, W0_calc, We_of_W0(W0_calc) / W0_calc, Wfuel_frac);
