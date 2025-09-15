import requests
import os
from datetime import datetime
from zoneinfo import ZoneInfo

LAT = 35.6895  # 東京
LON = 139.6917
API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise EnvironmentError("OPENWEATHER_API_KEY が設定されていません")

URL = "https://api.openweathermap.org/data/3.0/onecall"

def get_hourly_temps():
    params = {
        "lat": LAT,
        "lon": LON,
        "exclude": "minutely,daily,alerts,current",
        "units": "metric",
        "lang": "ja",
        "appid": API_KEY
    }
    res = requests.get(URL, params=params)
    if res.status_code != 200:
        raise RuntimeError(f"APIリクエスト失敗: {res.status_code}, 内容: {res.text}")

    data = res.json()
    hourly = data.get("hourly", [])
    forecast = []

    for h in hourly:
        dt = datetime.fromtimestamp(h["dt"], ZoneInfo("Asia/Tokyo"))
        hour_label = dt.strftime("%m/%d %H:%M")
        temp = h.get("temp")
        if temp is not None:
            forecast.append((hour_label, f"{temp:.1f}℃"))

    return forecast

def write_markdown(hourly_data):
    now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")
    md = f"# 🌡️ 東京の1時間ごとの気温予報（OpenWeatherMapより）\n\n"
    md += f"🕒 最終更新: **{now}**\n\n"
    md += "| 時間 | 気温 |\n|------|------|\n"
    for hour, temp in hourly_data:
        md += f"| {hour} | {temp} |\n"
    md += "\n> ※データは OpenWeatherMap を使用。1時間刻みで直近48時間の予報。"

    with open("weather_hourly_owm.md", "w", encoding="utf-8") as f:
        f.write(md)

if __name__ == "__main__":
    hourly_data = get_hourly_temps()
    write_markdown(hourly_data)
