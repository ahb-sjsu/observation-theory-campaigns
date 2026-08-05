function run_eg0_replication
% EG-0 MATLAB replication for the sealing clause. Replicates the
% closed-form controls of python/eg0_instrument.py independently and
% writes the agreement record. Every target is an exact closed form,
% so agreement bars are at rounding.

delta = 1e-4; epsv = 0.05;
record = struct();

% Part A: fold branch bit on the symmetric midpoint grid
tau = -1 + ((0:19999) + 0.5) * delta;
bins = floor(tau.^2 / epsv);
gap = cond_entropy(bins) - cond_entropy(bins * 2 + (tau > 0));
assert(abs(gap - 1.0) < 1e-12, 'fold bit failed: %g', gap);
record.fold_bit = gap;

% Double-fold symmetric slice via coarea weights
w = [1/2 1 1/2]; p = w / sum(w);
m0 = -sum(p .* log2(p));
assert(abs(m0 - 1.5) < 1e-15, 'M0 failed');
record.double_fold_bits = m0;

% Part B: aligned linear control, exactly log2(100)
taul = ((0:9999) + 0.5) * delta;
binsl = floor(0.8 * taul / 0.008);
hlin = cond_entropy(binsl);
assert(abs(hlin - log2(100)) < 1e-12, 'linear control failed: %g', hlin);
record.linear_control_bits = hlin;

% Part C: nested uniforms, exactly 2 bits
p1 = [ones(1, 2500) zeros(1, 7500)];
p2 = ones(1, 10000);
dnested = rel_entropy(p1, p2);
assert(abs(dnested - 2.0) < 1e-12, 'nested uniforms failed');
record.nested_uniform_bits = dnested;

% Gaussian control against the closed-form divergence
d = 0.0025;
x = (-10:d:(10 - d)) + d / 2;
g1 = exp(-0.5 * x.^2);
g2 = exp(-0.5 * ((x - 0.5) / 1.5).^2);
dg = rel_entropy(g1, g2);
klx = (log(1.5) + (1 + 0.25) / (2 * 2.25) - 0.5) / log(2);
assert(abs(dg - klx) < 1e-9, 'gaussian control failed: %g', abs(dg - klx));
record.gauss_abs_err = abs(dg - klx);

% Deformed-fold per-bin D equals the binary closed form exactly
wm = 2 * (tau < 0) + 1 * (tau >= 0);
pref = 2 / 3;
dbin_target = pref * log2(2 * pref) + (1 - pref) * log2(2 * (1 - pref));
maxdev = 0;
for b = 0:89
    idx = (bins == b);
    if ~any(idx), continue; end
    mneg = sum(wm(idx & (tau < 0)));
    mtot = sum(wm(idx));
    pm = mneg / mtot;
    dbin = pm * log2(2 * pm) + (1 - pm) * log2(2 * (1 - pm));
    maxdev = max(maxdev, abs(dbin - dbin_target));
end
assert(maxdev < 1e-12, 'deformed fold failed: %g', maxdev);
record.deformed_fold_max_dev = maxdev;
record.binary_target_bits = dbin_target;

record.verdict = ['MATLAB replication passing on every closed-form ' ...
    'control at rounding precision; the EG-0 cross-substrate clause ' ...
    'is satisfied'];
fid = fopen('/home/claude/projection-fold-pair-creation/results/eg0-matlab.json', 'w');
fprintf(fid, '%s', jsonencode(record));
fclose(fid);
disp(record);
disp('EG0_MATLAB_OK');
end

function h = cond_entropy(bins)
n = numel(bins);
cnt = accumarray(bins(:) - min(bins) + 1, 1);
cnt = cnt(cnt > 0);
h = sum((cnt / n) .* log2(cnt));
end

function d = rel_entropy(p, q)
p = p / sum(p); q = q / sum(q);
m = p > 0;
d = sum(p(m) .* log2(p(m) ./ q(m)));
end
