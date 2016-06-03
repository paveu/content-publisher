import os
from django.conf import settings
from srvup.celery import app
from django.core.mail import send_mail

@app.task()
def sendFeedbackEmail(email, message):
    subject = "Feedback from %s" % email
    return send_mail(subject, str(message), str(email), ['omega8@o2.pl'], fail_silently=False)
    