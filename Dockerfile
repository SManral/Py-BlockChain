FROM python:3
MAINTAINER Smriti Manral

WORKDIR /app

ADD . /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 80

# Run server.py when the container launches
CMD ["python3", "blockchain-api/server.py"]
