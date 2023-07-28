from celery import Celery
from celery.schedules import crontab

from conf import REDIS_CONNECTION, SCHEDULING_TZ


app = Celery('SAS', broker=REDIS_CONNECTION)

app.conf.result_backend = REDIS_CONNECTION

app.conf.beat_schedule = {
    'running': {
        'schedule': crontab(minute=0, hour=1),
        'task': 'scheduling.tasks.run'
    },
}

app.conf.timezone = SCHEDULING_TZ
