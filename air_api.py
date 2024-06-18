import requests
from urllib.parse import urlencode
import json
import pandas as pd
import datetime

def air_main(city):

    # 1. 기상청 Data 불러오기 
    url = 'http://apis.data.go.kr/B552584/ArpltnStatsSvc/getCtprvnMesureSidoLIst'
    sidoName = city
    searchCondition = "HOUR"
    serviceKey = 'kHVoQWfi7ynI0P68d5E1imQwzVIrPPU+jSWYQVNQ6YLEaCvlfGkGJHz3y7YW/siVjlEHCyq8TnAIl9F47csBng=='  # Replace with your actual valid service key
    pageNo = 1
    numOfRows = 100
    returnType = 'json'
    
    params = {
        "sidoName": sidoName,
        "searchCondition": searchCondition,
        "pageNo": pageNo,
        "numOfRows": numOfRows,
        "returnType": returnType,
        "serviceKey": serviceKey,
    }
    
    # URL parsing
    response = requests.get(url, params=params)
    
    # Check if the response is valid
    if response.status_code == 200:
        try:
            data = response.json()  # JSON file load하기 
            print(json.dumps(data, indent=4, ensure_ascii=False))  # Print the JSON structure
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON response")
            print("Response text:", response.text)
            return  # Exit the function without stopping the script
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        print("Response text:", response.text)
        return  # Exit the function without stopping the script
    
    # Ensure the 'response' and 'body' keys exist in the data
    if 'response' in data and 'body' in data['response'] and 'totalCount' in data['response']['body']:
        body = data['response']['body']
        if body['totalCount'] > 0:
            items = body['items']
            df = pd.DataFrame(items)  # Create DataFrame from items
            print(df.head())  # Print first few rows of the DataFrame to verify its structure
    
            # Ensure the required columns exist
            required_columns = ['cityName', 'pm10Value', 'pm25Value', 'dataTime']
            if all(column in df.columns for column in required_columns):
                df = df[required_columns]  # 필요한 열만 선택
                df = df.dropna()  # 결측값 제거
    
                # 날짜 필터링
                today = datetime.datetime.today().strftime('%Y-%m-%d')
                df['dataTime'] = pd.to_datetime(df['dataTime'])
                df = df[df['dataTime'].dt.strftime('%Y-%m-%d') == today]
    
                # 데이터 요약
                pm10_avg = df['pm10Value'].astype(float).mean()
                pm25_avg = df['pm25Value'].astype(float).mean()
                
                print(pm10_avg)
                print(pm25_avg)
                return pm10_avg, pm25_avg
    else:
        print("Error: 'response' or 'body' key not found in the data or no data available.")
        return  pm10_avg, pm25_avg
