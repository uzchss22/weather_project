from flask import Flask, request, render_template
from db_manager import get_weather_data


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


if __name__ == '__main__':
    app.run(debug=True)
