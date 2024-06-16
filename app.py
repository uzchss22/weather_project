from flask import Flask, request, render_template
from db_manager import get_weather_data
from apscheduler.schedulers.background import BackgroundScheduler

from weather_api import weather_scheduler
from db_manager import delete_db_scheduler, insert_notification, delete_user

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    region = request.form['region']
    city = request.form['city']
    weather_data = get_weather_data(region, city)
    return render_template('weather.html', weather=weather_data)

@app.route('/notification', methods=['POST'])
def notification_data_save():
    status = request.form['status'] # 알림 수신 동의 여부
    # ip주소 저장 로직.
    if 'X-Forwarded-For' in request.headers:
        user_ip = request.headers['X-Forwarded-For']  # 프록시를 통한 접속 감지
    else:
        user_ip = request.remote_addr

        
        
    if (status == "true"):                              # 알림 활성화 상태인경우 db에 ip, 시간 저장.
        timeset = request.form['alarmTime']
        insert_notification(user_ip, timeset)
    else:                                 # 비활성화로 제출 시 db에서 해당하는 ip가 있는지 조회 후 delete.
        delete_user(user_ip)    
    
    return render_template('index.html')
    
    
delete_db_scheduler() # 서버 시작 시 오래된 데이터 있으면 지움.

# weather_scheduler() # 


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(weather_scheduler, 'cron', hour="5", minute="30") # 매일 5시 30분에 api 요청
scheduler.add_job(delete_db_scheduler, 'cron', hour="0") # 매일 00시에 오래된 데이터 drop

scheduler.start()


        
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
