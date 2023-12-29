import logging
import pymysql
import uuid
import os
import datetime

logger = logging.getLogger(__name__)

class TorchServeDB:
    def __init__(self):
        self.connection =  pymysql.connect(
        host="docker-mysql",
        user="root",
        password="root",
        database="torchserve_db",
        cursorclass=pymysql.cursors.DictCursor,
    )

    def save_log(self, log):
        with self.connection.cursor() as cursor:
            try:
                timestamp = log["timestamp"]
                client_ip = log['client_ip']
                question = str(log['input_data'])
                answer = str(log['output_data'])

                sql = "INSERT INTO `torchserve_log` (`id`,`request_time`, `ip`, `question`, `answer`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (uuid.uuid4(), timestamp, client_ip, question, answer))
                self.connection.commit()

            except pymysql.Error as e:
                print(f"Error: {e}")


def log_and_save(func):
    def wrapper(self, *args, **kwargs):
        preds = func(self, *args, **kwargs)
        
        # 추론 정보 저장
        log_info = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "client_ip": self.context.get_request_header(0, "Host"),
            "input_data": self.input,
            "output_data": preds,
        }
        
        # DB에 요청 정보 기록
        logger.info(f"save logs : {log_info}")

        torchserve_db = TorchServeDB()
        torchserve_db.save_log(log_info)

        return preds
    return wrapper