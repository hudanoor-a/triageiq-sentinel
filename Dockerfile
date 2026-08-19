FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m textblob.download_corpora

COPY data/ data/
COPY triageiq/ triageiq/

RUN python triageiq/train.py

ENV MODEL_PATH=triageiq/models/triage_model.joblib

EXPOSE 5000

CMD ["python", "triageiq/app.py"]
