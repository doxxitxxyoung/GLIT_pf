# Currently written for cpu version

FROM pytorch/pytorch:0.4.1-cuda9-cudnn7-runtime


COPY . /root/example
WORKDIR /root/example
#RUN pip install pip -U && pip install -r requirements.txt
RUN pip install pip -U 

WORKDIR /root
USER root


RUN apt-get update
#RUN apt-get install sudo
#RUN apt-get install unzip
RUN apt install unzip
# Update to torch 1.1

RUN conda install pytorch-cpu==1.1.0 torchvision-cpu==0.3.0 cpuonly -c pytorch
#RUN conda install pytorch==1.1.0 torchvision==0.3.0 cudatoolkit=9.0 -c pytorch

RUN apt-get install g++

RUN pip install torch-scatter==1.1.2
RUN pip install torch-sparse==0.2.4
RUN pip install torch-cluster==1.2.4
#RUN pip install torch-spline-conv==1.1.0
RUN pip install torch-geometric==1.1.2
RUN conda install -c anaconda networkx==2.3
RUN conda install -c rdkit rdkit
RUN conda install -c anaconda scipy==1.2
RUN conda install -c anaconda networkx==2.3


RUN git clone https://github.com/doxxitxxyoung/GLIT_pf.git

# downloading data / models
RUN pip install gdown
WORKDIR GLIT_pf
WORKDIR data
RUN gdown https://drive.google.com/uc?id=1sTrPgiatGqKTjvxN5ppLxNO4iBKQ6snv
RUN unzip -o data.zip
RUN rm data.zip
RUN rm labeled_list_woAmbi_92742_70138_old.pkl

WORKDIR GLIT_pf
WORKDIR params
RUN gdown https://drive.google.com/uc?id=1EpAGz5Ztw3wKV-4H8nC4xF5hLwoCdixu
RUN unzip -o models.zip
RUN rm models.zip
WORKDIR GLIT_pf

#RUN unzip data.zip -d data
#RUN unzip models.zip -d models

# run flask server
RUN pip install flask
RUN python server.py
#CMD ["python", "server.py"]


#FLASK_ENV=development FLASK_APP=server.py flask run

#docker build -t doxxitxxyoung/glit_server .

