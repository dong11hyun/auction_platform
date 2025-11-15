import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('auction_platform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery Beat 스케줄
app.conf.beat_schedule = {
    'start-scheduled-auctions': {
        'task': 'core.tasks.auction_tasks.start_scheduled_auctions',
        'schedule': 60.0,  # 1분마다
    },
    'end-expired-auctions': {
        'task': 'core.tasks.auction_tasks.end_expired_auctions',
        'schedule': 60.0,  # 1분마다
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')