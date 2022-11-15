FROM python:3.8

RUN git clone https://github.com/Capstone-PlantHospital/PlantHospital-AI-Server.git

WORKDIR /PlanHospital-AI-Server

RUN git clone https://github.com/ultralytics/yolov5
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]