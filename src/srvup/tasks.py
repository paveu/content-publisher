import os
from django.conf import settings
from srvup.celery import app
from django.core.mail import send_mail

@app.task()
def sendFeedbackEmail(email, message):
    return send_mail('Feedback', str(message), settings.EMAIL_HOST_USER, [str(email)], fail_silently=False)
    