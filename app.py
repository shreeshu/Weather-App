from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = ''

weather_icon_map = {
    'sunny': 'sunny.png',
    'cloudy': 'cloudy.png',
    'rain': 'rainy.png',
    'snow': 'snowy.png',
    'overcast': 'overcast.png'
}

@app.route('/', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
        return render_template('weather.html', weather=weather_data)
    return render_template('weather.html', weather=None)

def get_weather(city):
    url = f'http://api.weatherstack.com/current?access_key={API_KEY}&query={city}'
    response = requests.get(url)
    data = response.json()
    if 'current' in data:
        weather_description = data['current']['weather_descriptions'][0].lower()
        icon_filename = weather_icon_map.get('cloudy', 'default.png')  # Default to 'cloudy' if not found

        for key in weather_icon_map.keys():
            if key in weather_description:
                icon_filename = weather_icon_map[key]
                break
        weather = {
            'city': data['location']['name'],
            'temperature': data['current']['temperature'],
            'description': data['current']['weather_descriptions'][0],
            'icon': icon_filename
        }
        return weather
    return None

if __name__ == '__main__':
    app.run(debug=True)