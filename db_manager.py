import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime, timedelta
import aiomysql



"""오늘 날짜를 'YYYYMMDD' 형식의 문자열로 반환하는 함수"""
def get_today_date():
    return datetime.now().strftime('%Y%m%d')

""" DB 연결 함수 """
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='weather-database.choogqsc8cqn.ap-northeast-2.rds.amazonaws.com',
            database='weather_database',
            user='admin',
            password='chlgur12',
            charset= 'utf8mb4'
        )
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

""" 전처리 된 데이터를 wtr_info 테이블에 삽입하는 함수 """ # 이 함수는 최적화를 위해 예외적으로 비동기화로 실행. (fetch_weather(), fetch_and_process_data(), insert_weather_data())
async def insert_weather_data(data):
    connection = await aiomysql.connect(host='weather-database.choogqsc8cqn.ap-northeast-2.rds.amazonaws.com', port=3306, user='admin', password='chlgur12', db='weather_database', charset='utf8mb4')
    try:
        async with connection.cursor() as cursor:
            insert_query = """
            INSERT INTO wtr_info (region, city, base_date, base_time, PTY, REH, RN1, T1H, VEC, WSD)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cleaned_data = [(tuple(None if pd.isna(x) else x for x in entry)) for entry in data]
            await cursor.executemany(insert_query, cleaned_data)
            await connection.commit()
            print(cursor.rowcount, "records inserted successfully.")
    except Exception as e:
        print("Failed to insert record into MySQL table", e)
    finally:
        connection.close()

""" 유저의 요청을 받으면 table에서 일치하는 행을 찾는 함수 """
def get_weather_data(region, city):
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT PTY, REH, RN1, T1H, VEC, WSD FROM wtr_info
        WHERE region=%s AND city=%s AND base_date=%s
        """
        cursor.execute(query, (region, city, get_today_date()))
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

""" 유저의 요청을 받으면 table에서 일치하는 행을 찾는 함수 """
def get_last_weather_data(region, city):
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT PTY, REH, RN1, T1H, VEC, WSD, date FROM wtr_info
        WHERE region=%s AND city=%s
        ORDER BY date DESC
        """
        cursor.execute(query, (region, city, get_today_date()))
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

""" base_date가 현재 날짜 기준으로 7일이 지난 데이터를 삭제하는 함수 """
def delete_old_weather_data():
    print("delete_old_weater_data() a executed")
    connection = connect_to_db()
    if connection is not None:
        try:
            cursor = connection.cursor()
            three_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
            delete_query = "DELETE FROM wtr_info WHERE base_date < %s"
            cursor.execute(delete_query, (three_days_ago,))
            connection.commit()
            print(cursor.rowcount, "records deleted successfully.")
        except Error as e:
            print("Failed to delete old records from MySQL table", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def delete_db_scheduler():
    delete_old_weather_data()
