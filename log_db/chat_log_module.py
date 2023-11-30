import pymysql
import uuid

class TorchServeDB:
    def __init__(self):
        self.connection =  pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="torchserve_db",
        cursorclass=pymysql.cursors.DictCursor,
    )

    def connect_to_db(self):
        try:
            with self.connection.cursor() as cursor:
                with open("/Users/bagdong-gyu/WorkSpace/VSCodeProject/torchserve_example/roberta/log_db/init.sql", "r") as sql_file:
                    sql_queries = sql_file.read()

                queries = sql_queries.split(";")

                for query in queries:
                    if query.strip() != "":
                        cursor.execute(query)

                self.connection.commit()
                print("SQL 파일 실행 완료")

        except pymysql.Error as e:
            print(f"Error: {e}")

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

                cursor.execute("SELECT * FROM `torchserve_log`")
                results = cursor.fetchall()
                
                for result in results:
                    print(result)
            except pymysql.Error as e:
                print(f"Error: {e}")

if __name__ == "__main__":

    torchserve_db = TorchServeDB()
    torchserve_db.connect_to_db()

    log_info = {
        'timestamp': '2023-11-28 23:40:30',
        'client_ip': 'localhost:8080',
        'input_data': ['dummy'],
        'output_data': ['dummy']
    }

    torchserve_db.save_log(log_info)
