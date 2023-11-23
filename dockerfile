FROM pytorch/torchserve:latest-cpu
# setting workdir in the container
WORKDIR /home/model-server/

# change user and change permissions
USER root
RUN chmod 777 -R . 

COPY ./docker_config.properties /home/model-server/config.properties
COPY ./model-store /home/model-server/model-store
COPY ./my_etc /home/model-server/my_etc

# start the server
CMD ["torchserve", "--start", "--ts-config", "/home/model-server/config.properties"]
# ENTRYPOIN
