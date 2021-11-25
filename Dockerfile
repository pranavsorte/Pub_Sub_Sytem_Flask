FROM python:3.9
ADD . /app
WORKDIR /app
EXPOSE 5001
EXPOSE 5002
EXPOSE 5003
EXPOSE 5004
RUN pip3 install -r requirements.txt
 