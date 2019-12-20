FROM doxxitxxyoung/glit_server:latest

COPY . /root

RUN pip install -r requirements.txt

WORKDIR /root

EXPOSE 80

ENV NAME glit_env

CMD ["python", "./root/server.py"]
