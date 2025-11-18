from datetime import datetime, timedelta
import time

def wait_for_alarm(hour, minute):
    now = datetime.now()
    alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # 알람 시간이 이미 지났으면 다음 날로 설정
    if alarm_time < now:
        alarm_time += timedelta(days=1)

    print(f"알람 대기 중... {alarm_time.strftime('%H:%M')}")

    while datetime.now() < alarm_time:
        time.sleep(10)
