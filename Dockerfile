FROM python:3.7.2-alpine3.9

RUN apt-get update && \
    apt-get install -y ffmpeg

COPY . /apophis/

RUN cd apophis/ && \
    pip install -r requirements.txt && \
    pip install -r requirements-e.txt

WORKDIR /apophis
ENTRYPOINT [ "python", "apophis" ]
