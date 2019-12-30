# Currently written for cpu version

#FROM pytorch/pytorch:0.4.1-cuda9-cudnn7-runtime
#FROM ubuntu:16.04
FROM gcr.io/glit-server-fast/glit-server-fast:v2


COPY . /root

WORKDIR /root
USER root


ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD ["uvicorn", "server_fastapi:app"]

