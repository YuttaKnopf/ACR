FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
WORKDIR /try
COPY requirements.txt .

RUN pip install -r requirements.txt


