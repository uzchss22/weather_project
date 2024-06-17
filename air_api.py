
import requests
from urllib.parse import urlencode
import pandas as pd
import datetime
from mysql.connector import Error

from db_manager import connect_to_db

def request_data(sidoName, serviceKey):
    """API로부터 데이터를 요청하고 JSON 형태로 반환"""
    url = 'http://apis.data.go.kr/B552584/ArpltnStatsSvc/getCtprvnMesureSidoLIst'
    params = {
        "sidoName": sidoName,
        "searchCondition": "HOUR",
        "pageNo": 1,
        "numOfRows": 100,
        "returnType": 'json',
        "serviceKey": serviceKey
    }
    params_encoded = urlencode(params)
    full_url = url + '?' + params_encoded
    response = requests.get(full_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"{sidoName} 데이터 요청 실패: {response.status_code}")
        return None

def process_and_save_data(data, cursor):
    """API 응답을 처리하고 데이터베이스에 저장"""
    if data and 'response' in data and 'body' in data['response']:
        body = data['response']['body']
        if body['totalCount'] > 0:
            items = body['items']
            df = pd.DataFrame(items)
            required_columns = ['cityName', 'pm10Value', 'pm25Value', 'dataTime']
            if all(column in df.columns for column in required_columns):
                df = df[required_columns]
                df = df.dropna()
                today = datetime.datetime.today().strftime('%Y-%m-%d')
                df['dataTime'] = pd.to_datetime(df['dataTime'])
                df = df[df['dataTime'].dt.strftime('%Y-%m-%d') == today]
                insert_data(df, cursor)
            else:
                print("필요한 컬럼이 누락됨")
        else:
            print("응답에 유효한 데이터가 없음")

def insert_data(df, cursor):
    insert_query = """
    INSERT INTO air_quality (cityName, pm10Value, pm25Value, dataTime)
    VALUES (%s, %s, %s, %s)
    """
    for _, row in df.iterrows():
        try:
            # 데이터 타입 체크 및 변환
            pm10_value = row['pm10Value'] if row['pm10Value'] else 0.0  # pm10Value가 빈 문자열인 경우 0.0으로 설정
            pm25_value = row['pm25Value'] if row['pm25Value'] else 0.0  # pm25Value가 빈 문자열인 경우 0.0으로 설정
            
            # float 타입으로 안전하게 변환
            pm10_value = float(pm10_value)
            pm25_value = float(pm25_value)
            
            # dataTime을 문자열로 변환
            formatted_date = row['dataTime'].strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(insert_query, (row['cityName'], pm10_value, pm25_value, formatted_date))
        except Exception as e:
            print(f"Insertion error: {e}")
            print(f"Failed row data: {row}")




def main():
    serviceKey = 'kHVoQWfi7ynI0P68d5E1imQwzVIrPPU+jSWYQVNQ6YLEaCvlfGkGJHz3y7YW/siVjlEHCyq8TnAIl9F47csBng=='
    cities = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종']
    try:
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        for city in cities:
            data = request_data(city, serviceKey)
            process_and_save_data(data, cursor)
            connection.commit()
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



if __name__ == '__main__':
    main()
