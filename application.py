from flask import Flask, request, render_template
from apscheduler.schedulers.background import BackgroundScheduler

from weather_api import weather_scheduler
from db_manager import delete_db_scheduler, get_weather_data, get_last_weather_data#, insert_notification, delete_user
#import air_api

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    region = request.form['region']
    city = request.form['city']
    weather_data = get_weather_data(region, city)
    return render_template('weather.html', weather=weather_data, region=region, city=city)


@app.route('/notification', methods=['POST'])
def notification_data_save():
    status = request.form['status'] # 알림 수신 동의 여부
    timeset = "24"
    if (status == "true"):
        timeset = request.form['alarmTime']
    return render_template('index.html', timeset=timeset)

    
    
delete_db_scheduler() # 서버 시작 시 오래된 데이터 있으면 지움.

# weather_scheduler() # 


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(weather_scheduler, 'cron', hour="5", minute="30") # 매일 5시 30분에 api 요청
scheduler.add_job(delete_db_scheduler, 'cron', hour="0") # 매일 00시에 오래된 데이터 drop
# scheduler.add_job(air_api.main(), 'cron', hour="5", minute="30")



scheduler.start()


        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', use_reloader=False)
