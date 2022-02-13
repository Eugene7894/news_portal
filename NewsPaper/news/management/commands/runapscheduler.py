import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import datetime, timedelta

from news.models import Post, Category

logger = logging.getLogger(__name__)


def news_sender():
    #  Your job processing logic here...
    for category in Category.objects.all():
        url = ''
        cat_subscribers = category.subscribers.all()
        week_news = Post.objects.filter(
            creationDate__range=[datetime.now(tz=None) - timedelta(days=7), datetime.now(tz=None)],
            postCategory=category
        )

        if week_news.exists():
            for week_new in week_news:
                url += f'{week_new.title} http://127.0.0.1:8000{week_new.get_absolute_url()}, \n'

            for subscriber in cat_subscribers:
                send_mail(
                    subject=f'Дайджест новостей за неделю по категории {category.categoryName}!',
                    message=f'Привет {subscriber.username}, дайджест новостей за неделю: {url}',
                    from_email='projects-mail-sf@yandex.ru',
                    recipient_list=[subscriber.email]
                )


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            news_sender,
            trigger=CronTrigger(day_of_week="mon", hour="08"),
            # отправляем письма подписчикам в понедельник в 8 утра
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="news_sender",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="09", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")