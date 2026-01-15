import schedule
import time
from datetime import datetime
from app import send_all_reminders


def job():
today = datetime.today().day
if today in [1, 5, 15]:
send_all_reminders()


schedule.every().day.at("09:00").do(job)


while True:
schedule.run_pending()
time.sleep(60)