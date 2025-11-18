import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import json
import os
import threading
import time
from summary.weather import get_weather
from summary.new import get_today_news
from memory.memory import get_today_events
from output.voice import speak

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_PATH = os.path.join(BASE_DIR, "memory.json")
# 설정 창 열기
def open_settings():
    config = load_config()
    settings_win = tk.Toplevel(root)
    settings_win.title("설정")
    settings_win.geometry("300x200")

    # 날씨 설정
    weather_var = tk.BooleanVar(value=config.get("enable_weather", True))
    tk.Checkbutton(settings_win, text="날씨 알림 활성화", variable=weather_var).pack(anchor="w", pady=5)

    # 뉴스 설정
    news_var = tk.BooleanVar(value=config.get("enable_news", True))
    tk.Checkbutton(settings_win, text="뉴스 알림 활성화", variable=news_var).pack(anchor="w", pady=5)

    def save_settings():
        new_config = {
            "enable_weather": weather_var.get(),
            "enable_news": news_var.get()
        }
        save_config(new_config)
        messagebox.showinfo("저장 완료", "설정이 저장되었습니다.")
        settings_win.destroy()

    tk.Button(settings_win, text="저장", command=save_settings).pack(pady=10)


# 메인 윈도우 생성
root = tk.Tk()
root.title("스마트 알람 챗봇")
root.geometry("500x700")

# memory.json 불러오기 / 저장하기
def load_memory():
    try:
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"alarms": [], "events": [], "enable_weather": True, "enable_news": True}

def save_memory(data):
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

#config.json 불러오기 / 저장하기
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"enable_weather": True, "enable_news": True}

def save_config(data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# 알람 저장
def save_alarm():
    try:
        hour = int(alarm_hour_entry.get())
        minute = int(alarm_minute_entry.get())
    except ValueError:
        messagebox.showerror("입력 오류", "숫자 형식의 시간과 분을 입력해주세요.")
        return

    new_alarm = {"hour": hour, "minute": minute}
    memory = load_memory()
    alarms = memory.get("alarms", [])
    alarms.append(new_alarm)
    memory["alarms"] = alarms
    save_memory(memory)

    update_alarm_list()
    wait_for_alarm(hour, minute)

# 알람 리스트 업데이트
def update_alarm_list():
    alarm_listbox.delete(0, tk.END)
    memory = load_memory()
    alarms = memory.get("alarms", [])
    for alarm in alarms:
        time_str = f"{alarm['hour']:02d}:{alarm['minute']:02d}"
        alarm_listbox.insert(tk.END, time_str)

# 알람 삭제
def delete_selected_alarm():
    selected_index = alarm_listbox.curselection()
    if not selected_index:
        messagebox.showwarning("경고", "삭제할 알람을 선택하세요.")
        return

    memory = load_memory()
    alarms = memory.get("alarms", [])
    del alarms[selected_index[0]]
    memory["alarms"] = alarms
    save_memory(memory)
    update_alarm_list()
    messagebox.showinfo("알림", "알람이 삭제되었습니다.")

# 알람 스레드 시작
def start_alarm_threads():
    memory = load_memory()
    for alarm in memory.get("alarms", []):
        wait_for_alarm(alarm["hour"], alarm["minute"])


# 알람 대기 및 실행
def wait_for_alarm(hour, minute):
    now = datetime.now()
    alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if alarm_time < now:
        alarm_time += timedelta(days=1)

    def alarm_thread():
        while datetime.now() < alarm_time:
            time.sleep(10)
        run_alarm_sequence()

    threading.Thread(target=alarm_thread, daemon=True).start()
    


def log_message(text):
    chat_log.config(state="normal")
    chat_log.insert(tk.END, f"{text}\n")
    chat_log.see(tk.END)
    chat_log.config(state="disabled")


def run_alarm_sequence():
    speak("스마트 알람이 울립니다.")
    log_message("🛎️ 스마트 알람이 울립니다.")

    memory = load_memory()
    config = load_config()

    if config.get("enable_weather"):
        weather = get_weather()
        if weather and weather.strip():
            speak("오늘 날씨입니다.")
            speak(weather)
            log_message(f"🌤️ 오늘 날씨: {weather}")


    events = get_today_events()
    if events and events.strip():
        speak("오늘 일정입니다.")
        log_message("📅 오늘 일정:")
        for line in events.split("\n"):
            speak(line)
            log_message(f" - {line}")
    else:
        speak("오늘 일정은 없습니다.")
        log_message("📅 오늘 일정 없음")

    if config.get("enable_news"):
        news = get_today_news()
        if news and news.strip():
            speak("오늘의 주요 뉴스입니다.")
            log_message("📰 오늘의 주요 뉴스:")
            for line in news.split("\n"):
                speak(line)
                log_message(f" - {line}")
        else:
            speak("오늘의 뉴스가 없습니다.")
            log_message("📰 오늘의 뉴스 없음")


# 일정 저장
def save_event():
    date = f"{year_var.get()}-{month_var.get()}-{day_var.get()}"
    time_ = f"{hour_var.get()}:{minute_var.get()}"
    summary = summary_entry.get()

    if not summary:
        messagebox.showwarning("입력 오류", "내용을 입력해주세요.")
        return

    memory = load_memory()
    memory["events"].append({"date": date, "time": time_, "summary": summary})
    save_memory(memory)
    refresh_event_list()
    messagebox.showinfo("일정 저장", f"{date} {time_} 일정이 저장되었습니다.")
    summary_entry.delete(0, tk.END)

# 일정 목록 갱신
def refresh_event_list():
    event_listbox.delete(0, tk.END)
    memory = load_memory()
    for e in memory["events"]:
        event_listbox.insert(tk.END, f"{e['date']} {e['time']} - {e['summary']}")

# 일정 삭제
def delete_selected_event():
    selected = event_listbox.curselection()
    if not selected:
        return
    index = selected[0]
    memory = load_memory()
    del memory["events"][index]
    save_memory(memory)
    refresh_event_list()

# -----------------------------
# 알람 입력
tk.Label(root, text="⏰ 알람 시간").grid(row=0, column=0)
alarm_hour_entry = tk.Entry(root, width=5)
alarm_hour_entry.grid(row=0, column=1)
tk.Label(root, text="시").grid(row=0, column=2)
alarm_minute_entry = tk.Entry(root, width=5)
alarm_minute_entry.grid(row=0, column=3)
tk.Label(root, text="분").grid(row=0, column=4)
tk.Button(root, text="알람 추가", command=save_alarm).grid(row=0, column=5)



# 알람 리스트
alarm_listbox = tk.Listbox(root, height=5, font=("Arial", 12))
alarm_listbox.grid(row=1, column=0, columnspan=6, pady=5)
tk.Button(root, text="선택된 알람 삭제", command=delete_selected_alarm).grid(row=2, column=0, columnspan=6)



# -----------------------------
# 일정 입력 (날짜 선택)
tk.Label(root, text="📅 날짜").grid(row=3, column=0)

year_var = tk.StringVar(value=str(datetime.now().year))
month_var = tk.StringVar(value=str(datetime.now().month).zfill(2))
day_var = tk.StringVar(value=str(datetime.now().day).zfill(2))

years = [str(y) for y in range(datetime.now().year, datetime.now().year + 2)]
months = [str(m).zfill(2) for m in range(1, 13)]
days = [str(d).zfill(2) for d in range(1, 32)]

tk.OptionMenu(root, year_var, *years).grid(row=3, column=1)
tk.Label(root, text="년").grid(row=3, column=2)
tk.OptionMenu(root, month_var, *months).grid(row=3, column=3)
tk.Label(root, text="월").grid(row=3, column=4)
tk.OptionMenu(root, day_var, *days).grid(row=3, column=5)
tk.Label(root, text="일").grid(row=3, column=6)

# 시간 선택
tk.Label(root, text="⏰ 시간").grid(row=4, column=0)

hour_var = tk.StringVar(value="07")
minute_var = tk.StringVar(value="00")

hours = [str(h).zfill(2) for h in range(0, 24)]
minutes = [str(m).zfill(2) for m in range(0, 60)]

tk.OptionMenu(root, hour_var, *hours).grid(row=4, column=1)
tk.Label(root, text="시").grid(row=4, column=2)
tk.OptionMenu(root, minute_var, *minutes).grid(row=4, column=3)
tk.Label(root, text="분").grid(row=4, column=4)

# 일정 내용
tk.Label(root, text="📝 내용").grid(row=5, column=0)
summary_entry = tk.Entry(root, width=40)
summary_entry.grid(row=5, column=1, columnspan=5)

tk.Button(root, text="일정 저장", command=save_event).grid(row=6, column=0, columnspan=6)

# 일정 리스트
event_listbox = tk.Listbox(root, width=60)
event_listbox.grid(row=7, column=0, columnspan=6)
tk.Button(root, text="선택한 일정 삭제", command=delete_selected_event).grid(row=8, column=0, columnspan=6)

# 채팅창 (알람 메시지 표시용)
chat_log = tk.Text(root, height=10, width=60, state="disabled", bg="#f9f9f9")
chat_log.grid(row=9, column=0, columnspan=6, pady=10)

# 설정 버튼
tk.Button(root, text="⚙️ 설정", command=open_settings).grid(row=10, column=0, columnspan=6, pady=10)

# -----------------------------
# 초기화
update_alarm_list()
refresh_event_list()
start_alarm_threads()  
root.mainloop()
