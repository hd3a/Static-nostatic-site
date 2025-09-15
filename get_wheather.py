import requests
from datetime import datetime
from zoneinfo import ZoneInfo

URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/130010.json"

def get_hourly_temps():
    res = requests.get(URL)
    data = res.json()

    # 気温データ（時間定義 + temps）
    time_series = next(ts for ts in data[1]['timeSeries'] if ts['dataType'] == 'temp')
    times = time_series['timeDefines']
    temps = time_series['areas'][0]['temps']

    # JSTで整形
    forecast = []
    for t, temp in zip(times, temps):
        dt = datetime.fromisoformat(t).astimezone(ZoneInfo("Asia/Tokyo"))
        hour = dt.strftime("%m/%d %H:%M")
        forecast.append((hour, temp + "℃"))

    return forecast

def write_markdown(hourly_data):
    now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")
    md = f"# 🌡️ 東京の1時間ごとの気温予報\n\n"
    md += f"🕒 最終更新: **{now}**\n\n"
    md += "| 時間 | 気温 |\n|------|------|\n"

    for hour, temp in hourly_data:
        md += f"| {hour} | {temp} |\n"

    md += "\n> ※気象庁のデータを使用。1〜2日分の気温を1時間ごとに更新。"
    
    with open("weather_hourly.md", "w", encoding="utf-8") as f:
        f.write(md)

if __name__ == "__main__":
    hourly_data = get_hourly_temps()
    write_markdown(hourly_data)
