import requests, json 
from os import getenv

api_key = getenv("weather_api_key")



def showWeather(city):
    city_name = city
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name +"&units=metric"
    response = requests.get(complete_url) 
      
    x = response.json() 
     
    if x["cod"] != "404": 
        wind = x["wind"]["speed"]
        y = x["main"] 
        current_temperature = y["temp"] 
        current_pressure = y["pressure"] 
        current_humidiy = y["humidity"] 
        z = x["weather"] 
        weather_description = z[0]["description"] 
      
        # print following values 
        return ("> Temperature  = " +
                        str(current_temperature) + 
              "\n> atmospheric pressure (in hPa unit) = " +
                        str(current_pressure) +
              "\n> humidity (in percentage) = " +
                        str(current_humidiy) +
              "\n> description = " +
                        str(weather_description) +
              "\n> wind speed = "+
                        str(wind)) 
      
    else: 
        return f"wtf is {city_name}? , City not found lol." 


