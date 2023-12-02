FROM pytorch/torchserve:latest-cpu

RUN pip install transformers
RUN pip install cryptography
RUN pip install pymysql

WORKDIR /home/model-server

EXPOSE 8080
EXPOSE 8081
EXPOSE 8082

COPY model-store /home/model-server/model-store
COPY my_etc /home/model-server/my_etc
COPY config.properties /home/model-server/config.properties
COPY log_db /home/model-server/log_db

ENV PYTHONPATH="/home/model-server/:$PYTHONPATH"
