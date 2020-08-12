from typing import List
from celery.decorators import task
from django.contrib.auth.models import User
import channels.layers
from asgiref.sync import async_to_sync

from app.backend.utils.email import Mailer
from app.models.task import Task
from app.backend.utils.enums import NewLine, FileType


@task(name="Export Practice", bind=True)
def export_practices(
    self, profile_id, name: str, description: str, os: str, file_type: str
):
    task = Task.objects.create(
        id=self.request.id, name=name, description=description, profile_id=profile_id
    )

    profile = User.objects.get(profile__pk=profile_id).profile
    file_name = profile.export_practices(
        NewLine.from_string(os), FileType.from_string(file_type)
    )

    task.complete = True
    profile.add_notification(
        f"export_practice_task_{file_type}",
        {"task_id": self.request.id, "file_name": file_name},
    )
    task.save()
    notifications_update.delay(profile.pk)


@task(name="Send Emails")
def send_email(to: List[str], subject: str, template: str, template_args):
    mail = Mailer()
    mail.send_messages(
        subject=subject,
        template=template,
        context=template_args,
        to_emails=["macpoule@gmail.com"],
    )


@task(name="Send notifications update")
def notifications_update(profile_id):
    profile = User.objects.get(profile__pk=profile_id).profile
    all_notifications = profile.notifications.filter(timestamp__gte=0).order_by(
        "timestamp"
    )

    async_to_sync(channels.layers.get_channel_layer().group_send)(
        "notifications",
        {
            "type": "notify_event",
            "data": {
                "names": [x.name for x in all_notifications],
                "data": [x.payload_json for x in all_notifications],
                "timestamps": [x.timestamp for x in all_notifications],
            },
        },
    )
