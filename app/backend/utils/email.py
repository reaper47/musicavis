from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from musicavis.settings import MUSICAVIS_ADMIN, MUSICAVIS_MAIL_SUBJECT_PREFIX


class Mailer:

    def __init__(self, from_email=MUSICAVIS_ADMIN):
        self.connection = mail.get_connection()
        self.from_email = from_email

    def send_messages(self, subject, template, context, to_emails):
        messages = self.__generate_messages(subject, template, context, to_emails)
        self.__send_mail(messages)

    def __send_mail(self, mail_messages):
        self.connection.open()
        self.connection.send_messages(mail_messages)
        self.connection.close()

    def __generate_messages(self, subject, template, template_args, to):
        content_txt = get_template(f'{template}.txt').render(template_args)
        content_html = get_template(f'{template}.html').render(template_args)

        messages = []
        for recipient in to:
            subject = f'[{MUSICAVIS_MAIL_SUBJECT_PREFIX}] {subject}'
            message = EmailMultiAlternatives(subject, content_txt, to=[recipient], from_email=self.from_email)
            message.attach_alternative(content_html, "text/html")
            messages.append(message)

        return messages
