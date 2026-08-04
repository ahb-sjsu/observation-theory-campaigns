FROM python:3.12-slim
WORKDIR /opt/projection-fold
COPY python/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY python/ /opt/projection-fold/python/
ENV PYTHONPATH=/opt/projection-fold/python
ENTRYPOINT ["python", "/opt/projection-fold/python/run_trial.py"]
