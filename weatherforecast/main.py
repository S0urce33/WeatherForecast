import requests
import PySimpleGUI as sg
from time import sleep

sg.theme('DarkBlue3')
sg.set_options(font=("Calibri", 12))

layout = [
    [sg.Text("Weather Forecast", font=("Calibri", 20), justification='center', expand_x=True, expand_y=True)],
    [sg.InputText(key='-CITY-', size=12), sg.Button('Get Weather'),],
    [sg.Text("Current weather in", key='Current weather in', expand_x=True, expand_y=True)],
    [sg.Text("Average Temperature:", key='Average Temperature:',expand_x=True, expand_y=True)],
    [sg.Text("Average Wind Speed:", key='Average Wind Speed:',expand_x=True, expand_y=True)],
    [sg.Button('Exit', size=12)],
    [sg.Text("Powered by WeatherAPI.com", font=("Calibri", 8), justification='center', expand_x=True, expand_y=True)]
]

window = sg.Window('WeatherForecast', layout, resizable=True, finalize=True)
API_KEY = "bee70387431d47fe999190928262009"

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break

    if event == 'Get Weather':
        city = values['-CITY-'].strip()
        if not city:
            sg.popup("Please enter a city first.")
            continue

       
        days = sg.popup_get_text(
            f"How many days of forecast for {city}?",
            title="Forecast Range",
            default_text=""
        )

        if days is None:  
            continue
        if not days.isdigit() or not (1 <= int(days) <= 10):
            sg.popup("Please enter a number between 1 and 10.")
            continue

        r = requests.get(
            f"http://api.weatherapi.com/v1/forecast.json"
            f"?key={API_KEY}&q={city}&days={days}&aqi=no&alerts=no"
        )
        data = r.json()

        if 'error' in data:
            sg.popup(f"Error: {data['error']['message']}")
            continue
        if int(days) > 1:
            window['Current weather in'].update(
            f"Current weather in {data['location']['name']}, {data['location']['region']}, {data['location']['country']}"
            )
            i = 0
            cycling = True
            while cycling:
                day_data = data['forecast']['forecastday'][i]['day']
                window['Average Temperature:'].update(
                    f" Average Temperature for day {i+1}: {day_data['avgtemp_c']}°C"
                )
                window['Average Wind Speed:'].update(
                    f" Average Wind Speed for day {i+1}: {day_data['maxwind_kph']} km/h"
                )

               
                cycle_event, _ = window.read(timeout=1000)

                if cycle_event in (sg.WINDOW_CLOSED, 'Exit'):
                    window.close()
                    exit()  

                i = (i + 1) % int(days)  
        else:
            window['Current weather in'].update(
                f"Current weather in {data['location']['name']}, {data['location']['region']}, {data['location']['country']}"
            )
            window['Average Temperature:'].update(f" Temperature: {data['forecast']['forecastday'][0]['day']['avgtemp_c']}°C")
            window['Average Wind Speed:'].update(f" Wind Speed: {data['forecast']['forecastday'][0]['day']['maxwind_kph']} km/h")    
window.close()
