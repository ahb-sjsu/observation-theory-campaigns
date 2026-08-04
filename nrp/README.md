# NRP execution notes

## Recommended starting point

Use CPU batch Jobs for PF-1 and PF-2. The current reference implementation is
small, deterministic, and easy to audit. Move to the vectorized CuPy path only
when profiling shows that trajectory integration, rather than storage or reduction,
is the bottleneck.

NRP's current documentation recommends finite Kubernetes Jobs for computation and
forbids batch workloads that merely sleep or wait for manual use. Resource requests
should closely match measured use; for large populations (roughly more than 100
pods or jobs), requests and limits must match. Keep a bounded live working set rather
than submitting the full campaign at once.

Official references checked when this package was drafted:

- https://nrp.ai/documentation/userdocs/running/jobs/
- https://nrp.ai/documentation/userdocs/start/policies/
- https://nrp.ai/documentation/userdocs/running/gpu-pods/
- https://nrp.ai/documentation/userdocs/tutorial/storage/

## Build and push

From the repository root:

```bash
docker build -t <registry>/<namespace>/projection-fold:0.1 .
docker push <registry>/<namespace>/projection-fold:0.1
```

Replace the image placeholder in `job-template.yaml` with the immutable image
digest when running a sealed campaign.

## Submit a smoke job

```bash
kubectl apply -f nrp/pvc.yaml
kubectl apply -f nrp/job-template.yaml
kubectl logs -f job/pf-smoke
```

The template writes one JSON evidence record to the PVC. For a campaign, a durable
backlog/controller should render or dispatch only a bounded number of jobs at once.

## Four campaign bounds

1. Active workers.
2. Existing Kubernetes Jobs and pending Pods.
3. I/O pressure and scratch use.
4. Unreduced evidence backlog.

A controller should issue Submit/Backoff/Abort decisions from these four witness
streams. A policy violation is a failed experiment.

## GPU path

`python/gpu_ensemble.py` uses CuPy if installed and NumPy otherwise. For NRP GPU
runs, choose a CUDA/CuPy image compatible with the scheduled GPU and request exactly
one GPU initially. Verify utilization before increasing the request. Do not treat
GPU type as scientifically irrelevant: record it, the CUDA runtime, precision, and
container digest in every trial.
