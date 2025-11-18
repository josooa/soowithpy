import os
import json
from datetime import datetime

# memory.py 기준으로 smart_alarm_chatbot 루트 경로 계산
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# gui 폴더 안의 memory.json 경로
MEMORY_PATH = os.path.join(ROOT_DIR, "gui", "memory.json")

def add_event(summary, hour, minute):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = f"{hour:02d}:{minute:02d}"


    new_event = {
        "date": date_str,
        "time": time_str,
        "summary": summary
    }

    try:
        with open(MEMORY_PATH, "r") as f:
            events = json.load(f)
    except FileNotFoundError:
        events = []

    events.append(new_event)

    with open(MEMORY_PATH, "w") as f:
        json.dump(events, f, indent=2)

    print(f"일정 추가됨: {summary} - {time_str}")

def get_today_events():
    try:
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)  
            events = data.get("events", [])
    except FileNotFoundError:
        return "오늘 일정은 없습니다."

    today = datetime.now().strftime("%Y-%m-%d")
    today_events = [e for e in events if e.get("date") == today]

    if not today_events:
        return "오늘 일정은 없습니다."

    result = ""
    for e in sorted(today_events, key=lambda x: x["time"]):
        result += f"- {e['time']} : {e['summary']}\n"

    return result.strip()
