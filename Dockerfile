FROM python:3.8

RUN git clone https://github.com/Capstone-PlantHospital/PlantHospital-AI-Server.git

WORKDIR /PlantHospital-AI-Server/

RUN git clone https://github.com/ultralytics/yolov5

WORKDIR /PlantHospital-AI-Server/yolov5
RUN pip install -qr requirements.txt flask torch

WORKDIR /PlantHospital-AI-Server

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]