FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/

CMD ["python3", "TGScript.py"]