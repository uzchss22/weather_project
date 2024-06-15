# weather_api.py
import requests
import pandas as pd
from datetime import datetime

from db_manager import insert_weather_data    

# API 키 및 기본 URL, 날짜, 시간 설정
API_KEY = "Rvot3cGqSgS6Ld3BqioE_w"
BASE_URL = "https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtNcst?"
BASE_TIME = "0400" # 예보 api인데 익일 해당 시간 이전만 데이터 받아짐.,.,
CSV_FILE_PATH = './data/region_data.csv'


"""오늘 날짜를 'YYYYMMDD' 형식의 문자열로 반환하는 함수"""
def get_today_date():
    return datetime.now().strftime('%Y%m%d')

""" api를 호출하고 db에 저장할 데이터셋을 전처리하는 함수 """
def fetch_and_process_weather_data(api_key, base_url, base_time, csv_file_path):
    print("fetch_and_process_weather_data() a executed")
    base_date = get_today_date()  # 매일 호출될 때마다 오늘 날짜로 갱신
    df = pd.read_csv(csv_file_path)
    weather_data_to_insert = []

    # API 호출 및 결과 처리
    for index, row in df.iterrows():
        nx, ny, region, city = row['nx'], row['ny'], row['region'], row['city']
        api_url = f"{base_url}authKey={api_key}&dataType=JSON&numOfRows=10&pageNo=1&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            items = data['response']['body']['items']['item']
            category_values = {}
            for item in items:
                category = item['category']
                obsrValue = item['obsrValue']
                category_values[category] = obsrValue
            
            # db에 저장할 데이터 전처리
            weather_data_to_insert.append((
                region, city, base_date, base_time,
                category_values.get('PTY'), category_values.get('REH'), category_values.get('RN1'), category_values.get('T1H'), category_values.get('VEC'), category_values.get('WSD')
            ))
        else:
            print(f"Error fetching data for ({nx}, {ny}): {response.status_code}")

    if weather_data_to_insert:
        insert_weather_data(weather_data_to_insert)

def weather_scheduler():
    fetch_and_process_weather_data(API_KEY, BASE_URL, BASE_TIME, CSV_FILE_PATH)