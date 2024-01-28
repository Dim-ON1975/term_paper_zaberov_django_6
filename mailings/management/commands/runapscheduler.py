# запуск из консоли командой python manage.py runapscheduler
import logging
import datetime

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)


def my_job():
    #  Логика обработки вашего задания здесь...
    pass


def delete_old_job_executions(max_age=604_800):
    """
    Удаляет из базы данных записи выполнения заданий APScheduler старше `max_age`.
    Это помогает предотвратить заполнение базы данных старыми историческими записями, которые не являются
    дольше полезными.
    :param max_age: Максимальный срок хранения истории записей выполнения заданий.
                    По умолчанию 7 дней."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Запуск планировщика."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Каждые 10 секунд
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена задача «my_job».")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Полночь понедельника, перед началом следующей рабочей недели.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Добавлено еженедельное задание: delete_old_job_executions."
        )

        try:
            logger.info("Запуск планировщика...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Остановка планировщика...")
            scheduler.shutdown()
            logger.info("Планировщик успешно закрылся!")
