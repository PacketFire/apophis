FROM python:3.7.2-stretch

RUN apt-get update && \
    apt-get install -y ffmpeg opus-tools

COPY . /apophis/

RUN cd apophis/ && \
    pip install -r requirements.txt && \
    pip install -r requirements-e.txt

WORKDIR /apophis
ENTRYPOINT [ "python", "apophis" ]
