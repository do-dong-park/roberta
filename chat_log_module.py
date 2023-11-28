import pymysql

def save_request_info(request_info):
    # 여기에는 실제로 사용하는 데이터베이스와 연결하여 요청 정보를 저장하는 코드가 들어갑니다
    
    pass


if __name__ == "__main__":

    # MySQL 연결 정보
    host = "localhost"
    port = 3306
    user = "root"
    password = "password"
    database = "my_database"

    # MySQL 연결
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )

    # MySQL 연결 확인
    print(connection)