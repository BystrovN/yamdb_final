FROM python:3.8.15-slim
WORKDIR /app
COPY . .
RUN pip3 install -r ./requirements.txt --no-cache-dir
CMD ["gunicorn", "api_yamdb.api_yamdb.wsgi:application", "--bind", "0:8000" ]
