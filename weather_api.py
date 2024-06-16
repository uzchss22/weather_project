# weather_api.py
# import requests
import pandas as pd
from datetime import datetime
import aiohttp
import asyncio

from db_manager import insert_weather_data    

# API 키 및 기본 URL, 날짜, 시간 설정
API_KEY = "Rvot3cGqSgS6Ld3BqioE_w"
BASE_URL = "https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtNcst?"
BASE_TIME = "0400" # 예보 api인데 익일 해당 시간 이전만 데이터 받아짐.,.,
CSV_FILE_PATH = './data/region_data.csv'



""" api를 호출하고 db에 저장할 데이터셋을 전처리하는 함수 """ # 이 함수는 최적화를 위해 예외적으로 비동기화로 실행. (fetch_weather(), fetch_and_process_data(), insert_weather_data())
async def fetch_weather(session, url):
    async with session.get(url) as response:
        return await response.json()

async def fetch_and_process_weather_data(api_key, base_url, base_time, csv_file_path): # 이 함수는 최적화를 위해 예외적으로 비동기화로 실행. (fetch_weather(), fetch_and_process_data(), insert_weather_data())

    print("fetch_and_process_weather_data() 실행됨")
    base_date = datetime.now().strftime('%Y%m%d')  # 오늘 날짜 갱신
    df = pd.read_csv(csv_file_path)
    weather_data_to_insert = []
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for index, row in df.iterrows():
            nx, ny, region, city = row['nx'], row['ny'], row['region'], row['city']
            url = f"{base_url}authKey={api_key}&dataType=JSON&numOfRows=10&pageNo=1&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}"
            tasks.append(fetch_weather(session, url))
        
        responses = await asyncio.gather(*tasks)
        
        for response, row in zip(responses, df.itertuples()):
            if response['response']['header']['resultCode'] == '00':
                items = response['response']['body']['items']['item']
                category_values = {item['category']: item['obsrValue'] for item in items}
                weather_data_to_insert.append((
                    row.region, row.city, base_date, base_time,
                    category_values.get('PTY'), category_values.get('REH'), category_values.get('RN1'), category_values.get('T1H'), category_values.get('VEC'), category_values.get('WSD')
                ))
            else:
                print(f"데이터 수신 오류 ({row.nx}, {row.ny}): {response['response']['header']['resultCode']}")

    if weather_data_to_insert:
        await insert_weather_data(weather_data_to_insert)

def weather_scheduler():
    asyncio.run(fetch_and_process_weather_data(API_KEY, BASE_URL, BASE_TIME, CSV_FILE_PATH))



