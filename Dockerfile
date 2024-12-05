FROM python:3.13.0

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install .

ENTRYPOINT [ "python", "src/main.py"]
