FROM python:3.9

WORKDIR /app
COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install streamlink
RUN apt-get -y update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN chmod a+x /app/run.sh

ENTRYPOINT ["/app/run.sh"]