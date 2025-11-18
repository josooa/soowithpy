import requests

API_KEY = "cac8ac2a577f7f41e852564460e72908"
CITY = "Seoul"

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=kr"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            description = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            return (f"{CITY}의 날씨는 {description}, "
                    f"기온은 {temp}도, 체감온도 {feels_like}도, "
                    f"습도 {humidity}% 입니다.")
        else:
            return f"날씨 정보를 가져올 수 없습니다. (에러 코드: {response.status_code})"
    except Exception as e:
        return f"날씨 정보를 가져오는 중 오류 발생: {e}"
