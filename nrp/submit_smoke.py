#!/usr/bin/env python3
"""Submit the PF-0 NRP CPU smoke job via the nats-bursting client."""
import json
import sys

sys.path.insert(0, "/home/claude/src/nats-bursting/python")

from nats_bursting.client import Client
from nats_bursting.descriptor import JobDescriptor, Resources, Volume

SCENARIO = {
    "model": "toy_hamiltonian",
    "omega_t": 1.0,
    "omega_u": 1.2,
    "lambda": 0.1,
    "g": 0.25,
    "field": 1.0,
    "t0": 0.0,
    "pt0": 1.0,
    "x0": 0.0,
    "px0": 0.2,
    "u0": 0.1,
    "pu0": 0.0,
    "dt": 0.001,
    "tau_max": 40.0,
}

shell = (
    "pip install --quiet --no-warn-script-location numpy && "
    "cd /work && "
    "python3 run_trial.py --scenario-json '" + json.dumps(SCENARIO) + "' "
    "--output /tmp/pf-smoke.json && "
    "echo '===RECORD-BEGIN===' && cat /tmp/pf-smoke.json && echo && "
    "echo '===RECORD-END==='"
)

descriptor = JobDescriptor(
    name="pf-smoke",
    image="python:3.12-slim",
    command=["sh", "-c", shell],
    env={"CODE_COMMIT": "cb50e60", "PYTHONDONTWRITEBYTECODE": "1"},
    resources=Resources(cpu="1", memory="2Gi"),
    labels={"app": "projection-fold", "stage": "pf0-smoke"},
    backoff_limit=0,
    volumes=[
        Volume(
            name="code",
            mount_path="/work",
            read_only=True,
            config_map="pf-smoke-code",
        )
    ],
)

with Client() as client:
    result = client.submit_and_wait(descriptor, timeout=120.0)
    print("job_id:", result.job_id)
    print("accepted:", result.accepted)
    print("state:", result.status.state if result.status else None)
    print("k8s_job:", result.k8s_job_name)
