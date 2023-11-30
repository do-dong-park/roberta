FROM pytorch/torchserve:latest-cpu

RUN pip install transformers
RUN pip install pymysql

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=torchserve_db
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=root

# 초기 SQL 스크립트 복사
COPY ./log_db/init.sql /docker-entrypoint-initdb.d/

# 컨테이너가 시작될 때 초기화 스크립트 실행
RUN chmod +r /docker-entrypoint-initdb.d/init.sql