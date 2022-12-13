from datetime import datetime
import time 

from apscheduler.schedulers.blocking import BlockingScheduler


time_now = datetime.now()
print(time_now)

def tarea():
    print ("Esta es mi tarea.")

    
def tasks():
    scheduler = BlockingScheduler()
    scheduler.add_job(tarea, "cron", hour=16, minute=22, second=50)
    scheduler.start()

tasks()

# import time
# from apscheduler.schedulers.blocking import BlockingScheduler

# scheduler = BlockingScheduler()

# @scheduler.scheduled_job('cron', hour=16, minute=37)
# def tarea():
#     print ("Esta es mi tarea.")
#     scheduler.shutdown()

# def otra_cosa():
#     print("Otra cosa")

# try:
#     scheduler.start()
#     otra_cosa()

# except KeyboardInterrupt:
#     scheduler.shutdown()
#     print("fin")