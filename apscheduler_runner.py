import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cp_manager.settings')
django.setup()

from apscheduler.schedulers.background import BackgroundScheduler
import time
from cp.cron import check_health, fetch_problem

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_problem, 'cron', hour=6, minute=0)
    scheduler.add_job(check_health, 'interval', minutes=0.1)
    scheduler.start()
    print("APScheduler started. fetch_problem will run every day at 06:00.")
    try:
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("APScheduler stopped.")
