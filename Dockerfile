FROM python:3.7.2-stretch

RUN apt-get update && \
    apt-get install -y ffmpeg opus-tools

COPY . .

RUN pip install -r requirements.txt && \
    pip install -r requirements-e.txt

ENTRYPOINT [ "python", "apophis" ]
