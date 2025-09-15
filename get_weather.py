import requests
from datetime import datetime
from zoneinfo import ZoneInfo

CITY_ID = "130010"  # 東京の都市ID
API_URL = f"https://weather.tsukumijima.net/api/forecast/city/{CITY_ID}"

def get_hourly_temps():
    response = requests.get(API_URL)
    response.raise_for_status()  # エラーチェック

    data = response.json()
    time_series = data['timeSeries']
    hourly_data = []

    for ts in time_series:
        if ts['dataType'] == 'temp':
            times = ts['timeDefines']
            temps = ts['areas'][0]['temps']
            for time, temp in zip(times, temps):
                dt = datetime.fromisoformat(time).astimezone(ZoneInfo("Asia/Tokyo"))
                hourly_data.append((dt.strftime("%m/%d %H:%M"), f"{temp}℃"))

    return hourly_data

def write_markdown(hourly_data):
    now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")
    md_content = f"# 🌡️ 東京の1時間ごとの気温予報\n\n"
    md_content += f"🕒 最終更新: **{now}**\n\n"
    md_content += "| 時間 | 気温 |\n|------|------|\n"
    for hour, temp in hourly_data:
        md_content += f"| {hour} | {temp} |\n"
    md_content += "\n> ※データは weather.tsukumijima.net を使用。"

    with open("weather_hourly.md", "w", encoding="utf-8") as f:
        f.write(md_content)

if __name__ == "__main__":
    hourly_data = get_hourly_temps()
    write_markdown(hourly_data)
