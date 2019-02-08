FROM python:3.7.2-stretch

RUN apt-get update && \
    apt-get install -y ffmpeg opus-tools && \
    wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/5.2.4/flyway-commandline-5.2.4-linux-x64.tar.gz | tar xvz && \
    mv ./flyway-5.2.4/flyway /usr/local/bin

COPY . .

RUN pip install -r requirements.txt && \
    pip install -r requirements-e.txt

ENTRYPOINT [ "python", "apophis" ]
