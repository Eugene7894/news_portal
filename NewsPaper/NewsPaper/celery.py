import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Добавляем расписание, по которому будет запускаться задача(по пн в 8.00)
app.conf.beat_schedule = {
    'send_mail_every_monday_8am': {
        'task': 'news.tasks.send_mail_every_monday',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}