FROM python:3.12

WORKDIR /app

COPY setup-db/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/todo/ ./todo/

COPY setup-db/setup.py .

CMD ["python", "setup.py"]
