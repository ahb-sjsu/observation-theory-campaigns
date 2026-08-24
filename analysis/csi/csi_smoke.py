"""Sionna 1.2 API smoke test for the CSI cell: real 5G LDPC coded QAM over
AWGN (one BLER point) + a TDL Doppler fading sequence. Prints shapes so the
full cell is written against the verified API."""
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import numpy as np
import tensorflow as tf
from sionna.phy.fec.ldpc import LDPC5GEncoder, LDPC5GDecoder
from sionna.phy.mapping import Mapper, Demapper, BinarySource
from sionna.phy.channel import AWGN
from sionna.phy.channel.tr38901 import TDL

k, R = 1024, 0.5
n = int(round(k / R))
qm = 4
enc = LDPC5GEncoder(k, n)
dec = LDPC5GDecoder(enc, num_iter=20, hard_out=True)
mapper = Mapper("qam", qm)
demapper = Demapper("app", "qam", qm)
src = BinarySource()
awgn = AWGN()

bs = 200
b = src([bs, k])
c = enc(b)
x = mapper(c)
esno_db = 6.0
no = tf.pow(10.0, -esno_db / 10.0)
try:
    y = awgn(x, no)
except Exception as e:
    print("awgn(x,no) failed:", e, "-> trying [x,no]")
    y = awgn([x, no])
llr = demapper(y, no)
bhat = dec(llr)
bler = float(tf.reduce_mean(
    tf.cast(tf.reduce_any(tf.not_equal(b, bhat), axis=1), tf.float32)))
print("LDPC chain OK | b", b.shape, "c", c.shape, "x", x.shape,
      "y", y.shape, "llr", llr.shape, "bhat", bhat.shape,
      "| BLER@%.0fdB=%.3f" % (esno_db, bler))

# TDL Doppler fading sequence
c0, fc, fd = 3e8, 3.5e9, 200.0
v = fd * c0 / fc
tdl = TDL(model="A", delay_spread=30e-9, carrier_frequency=fc,
          min_speed=v, max_speed=v)
out = tdl(1, 2000, 1000.0)
a = out[0] if isinstance(out, (tuple, list)) else out
print("TDL a", a.shape)
# collapse everything but time; narrowband gain = sum over paths
a = tf.squeeze(a)                        # -> (num_paths, num_time) for SISO
print("TDL a squeezed", a.shape)
h = tf.reduce_sum(a, axis=0)             # narrowband: sum path gains
p = np.abs(h.numpy()) ** 2
print("h", h.shape, "| mean|h|^2=%.3f" % p.mean(),
      "| snr swing dB ~ %.1f" % (10 * np.log10(p.max() / max(p.min(), 1e-9))))
print("v=%.2f m/s for fd=%.0fHz @ %.1fGHz" % (v, fd, fc / 1e9))
