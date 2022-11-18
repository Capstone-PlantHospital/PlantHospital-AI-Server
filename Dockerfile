FROM python:3.8

RUN git clone https://github.com/Capstone-PlantHospital/PlantHospital-AI-Server.git

WORKDIR /PlantHospital-AI-Server/

RUN git clone https://github.com/ultralytics/yolov5
RUN mkdir -p /PlantHospital-AI-Server/temp

WORKDIR /PlantHospital-AI-Server/yolov5

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -qr requirements.txt flask torch boto3

WORKDIR /PlantHospital-AI-Server

EXPOSE 5000

ENTRYPOINT ["nohup", "python", "app.py", "&"]