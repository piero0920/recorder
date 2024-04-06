FROM python:3.9

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --user -U streamlink
RUN apt-get -y update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . .
RUN chmod a+x run.sh

CMD ["/app/run.sh"]