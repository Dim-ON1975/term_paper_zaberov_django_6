from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job

scheduler = BackgroundScheduler()


@register_job(scheduler, 'interval', seconds=3)
def task():
    print('gogogo')


try:
    scheduler.start()
    print('Планировщик запущен!')
except Exception as e:
    print(e)
scheduler.shutdown()
