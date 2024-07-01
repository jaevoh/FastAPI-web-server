from fastapi import FastAPI, Request
import requests
import ipinfo

app = FastAPI()

WEATHER_API_KEY = "bc9756da9c4b44e9b89212131243006"


def get_temperature(city):
    try:
        weather_api_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
        response = requests.get(weather_api_url)
        print(f"WeatherAPI response status code: {response.status_code}")
        print(f"WeatherAPI response: {response.json()}")
        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data['current']['temp_c']
            return temperature
        else:
            print("Failed to fetch temperature data")
            return None
    except Exception as e:
        print(f"An error occurred while fetching temperature: {e}")
        return None


def get_location(client_ip):
    try:
        location_api_url = f"http://ipinfo.io/{client_ip}/json"
        response = requests.get(location_api_url)
        print(f"ipinfo.io response status code: {response.status_code}")
        print(f"ipinfo.io response: {response.json()}")
        if response.status_code == 200:
            location_data = response.json()
            city = location_data.get("city", "Unknown")
            return city
        else:
            print("Failed to fetch location data")
            return "Unknown"
    except Exception as e:
        print(f"An error occurred while fetching location: {e}")
        return "Unknown"


@app.get("/api/hello")
async def hello(request: Request, visitor_name: str):
    client_ip = request.client.host

    city = get_location(client_ip)

    temperature = get_temperature(city)
    if temperature is None:
        temperature = "unknown"

    return {
        "client_ip": client_ip,
        "location": city,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
    }
