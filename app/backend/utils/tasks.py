from typing import List
from rq import get_current_job
from django_rq import job
from celery.decorators import task

from app.backend.utils.email import Mailer
from app.models.task import Task


@job
def export_practices(user, name, description, os, file_type):
    job = get_current_job()

    task = Task.objects.create(id=job.get_id(), name=name, description=description, user=user)

    _set_task_file_name(job, task, file_type)
    file_name = user.export_practices(os, file_type)
    _set_task_file_name(job, task, file_type, file_name)


def _set_task_progress(job, task, progress, **kwargs):
    if job:
        job.meta['progress'] = progress
        job.save_meta()

        task.user_object.add_notification('task_progress', {'task_id': job.get_id(), 'progress': progress, **kwargs})

        if progress >= 100:
            task.complete = True

        task.save()


def _set_task_file_name(job, task, file_type, file_name=None):
    if job:
        job.meta['file_name'] = file_name
        job.save_meta()

        task.user.add_notification(f"export_practice_task_{file_type.value}",
                                   {'task_id': job.get_id(), 'file_name': file_name})

        if file_name:
            task.complete = True

        task.save()


@task(name="Send Emails")
def send_email(to: List[str], subject: str, template: str, template_args):
    mail = Mailer()
    mail.send_messages(
        subject=subject,
        template=template,
        context=template_args,
        to_emails=['macpoule@gmail.com']
    )
