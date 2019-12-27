# Currently written for cpu version

FROM pytorch/pytorch:0.4.1-cuda9-cudnn7-runtime
#FROM ubuntu:16.04


COPY . /root

#RUN pip install pip -U && pip install -r requirements.txt
RUN pip install pip -U 

WORKDIR /root
USER root


RUN apt-get update
#RUN apt-get install sudo
#RUN apt-get install unzip
RUN apt install unzip
# Update to torch 1.1

RUN conda install pytorch-cpu==1.1.0 cpuonly -c pytorch
#RUN conda install pytorch-cpu==1.1.0 torchvision-cpu==0.3.0 cpuonly -c pytorch
#RUN conda install pytorch==1.1.0 torchvision==0.3.0 cudatoolkit=9.0 -c pytorch

RUN apt-get install g++

RUN pip install torch-scatter==1.1.2
RUN pip install torch-sparse==0.2.4
RUN pip install torch-cluster==1.2.4
#RUN pip install torch-spline-conv==1.1.0
RUN pip install torch-geometric==1.1.2
RUN conda install -c anaconda networkx==2.3
#RUN conda install -c rdkit rdkit
RUN conda install -c anaconda scipy==1.2
RUN conda install -c anaconda numpy==1.16

RUN pip install flask
RUN pip install fastapi pydantic uvicorn
RUN pip install email-validator


RUN git clone https://github.com/doxxitxxyoung/GLIT_pf.git

#COPY /GLIT_pf/* ./root
#RUN mv ./GLIT_pf/* .
RUN (cd GLIT_pf && tar c .) | (tar xf -)

# downloading data / models
RUN pip install gdown
#WORKDIR ./root

WORKDIR data
#RUN gdown https://drive.google.com/uc?id=1sTrPgiatGqKTjvxN5ppLxNO4iBKQ6snv
#RUN unzip -o data.zip
#RUN rm data.zip
#RUN rm labeled_list_woAmbi_92742_70138_old.pkl

RUN gdown https://drive.google.com/uc?id=146o7-P6ElDZHu_KlS-VMu6X8_FeWHZOc
RUN unzip -o data_serve.zip
RUN rm data_serve.zip
#RUN rm labeled_list_woAmbi_92742_70138_old.pkl
WORKDIR ../

WORKDIR params
RUN gdown https://drive.google.com/uc?id=1EpAGz5Ztw3wKV-4H8nC4xF5hLwoCdixu
RUN unzip -o models.zip
RUN rm models.zip
WORKDIR ../

#RUN unzip data.zip -d data
#RUN unzip models.zip -d models

# run flask server

#RUN python server.py
#CMD ["python", "server.py"]


#EXPOSE 80

#ASCII ISSUE
#RUN export LC_ALL=C.UTF-8
#RUN export LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

#CMD ["uvicorn", "server_fastapi:app", "--reload"]
#CMD uvicorn server_fastapi:app --port 8044
#CMD ["uvicorn", "server_fastapi:app", "--reload", "--port", "8044"]
CMD ["uvicorn", "server_fastapi:app"]

#CMD ["uvicorn", "--host", "0.0.0.0", "--port", "80"]


#FLASK_ENV=development FLASK_APP=server.py flask run

#docker build -t doxxitxxyoung/glit_server .

