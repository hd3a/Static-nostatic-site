import requests
from datetime import datetime
from zoneinfo import ZoneInfo

CITY_ID = "130010"  # 東京
API_URL = f"https://weather.tsukumijima.net/api/forecast/city/{CITY_ID}"

def get_forecast():
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()

    forecasts = data.get("forecasts", [])
    hourly_data = []

    for forecast in forecasts:
        date_label = forecast.get("dateLabel")
        date = forecast.get("date")
        telop = forecast.get("telop")
        temp_max = forecast.get("temperature", {}).get("max", {}).get("celsius")
        temp_min = forecast.get("temperature", {}).get("min", {}).get("celsius")
        chance_rain = forecast.get("chanceOfRain", {})
        # 6時間ごとの降水確率
        T00_06 = chance_rain.get("T00_06")
        T06_12 = chance_rain.get("T06_12")
        T12_18 = chance_rain.get("T12_18")
        T18_24 = chance_rain.get("T18_24")

        hourly_data.append({
            "date_label": date_label,
            "date": date,
            "telop": telop,
            "temp_max": temp_max,
            "temp_min": temp_min,
            "chance_rain": {
                "0-6": T00_06,
                "6-12": T06_12,
                "12-18": T12_18,
                "18-24": T18_24
            }
        })

    return hourly_data

def write_markdown(hourly_data):
    now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")
    md = f"# 🌦️ 東京の天気予報（6時間ごと）\n\n"
    md += f"🕒 最終更新: **{now}**\n\n"
    md += "| 日付 | 天気 | 最高気温 | 最低気温 | 降水確率 0-6 | 6-12 | 12-18 | 18-24 |\n"
    md += "|------|------|----------|----------|------------|------|------|------|\n"

    for forecast in hourly_data:
        md += f"| {forecast['date_label']} ({forecast['date']}) | {forecast['telop']} | {forecast['temp_max'] or '-'}℃ | {forecast['temp_min'] or '-'}℃ | {forecast['chance_rain']['0-6'] or '-'} | {forecast['chance_rain']['6-12'] or '-'} | {forecast['chance_rain']['12-18'] or '-'} | {forecast['chance_rain']['18-24'] or '-'} |\n"

    md += "\n> ※データは weather.tsukumijima.net を使用。6時間ごとの降水確率と日ごとの最高/最低気温。"

    with open("weather_6hourly.md", "w", encoding="utf-8") as f:
        f.write(md)

if __name__ == "__main__":
    data = get_forecast()
    write_markdown(data)
