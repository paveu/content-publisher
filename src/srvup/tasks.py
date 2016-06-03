import os
from django.conf import settings
from srvup.celery import app
from django.core.mail import send_mail

@app.task()
def sendFeedbackEmail(email, message):
    return send_mail('Feedback from content-publisher', str(message), str(email), ['omega8@o2.pl'], fail_silently=False)
    