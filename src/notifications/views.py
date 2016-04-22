import json
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, Http404, HttpResponseRedirect, redirect, get_object_or_404

from .models import Notification


@login_required
def all(request):
    """
    Get all notification for particular user. It mixes read and unread messages
    """
    notifications = Notification.objects.all_for_user(request.user)
    context = {"notifications": notifications,
               }
    return render(request, "notifications/all.html", context)


@login_required
def read(request, id):
    """
    It marks particular notification as a read only if it's unread
    """
    notification = get_object_or_404(Notification, id=id)
    try:
        # getting next value i.e. : /notifications/read/11/?next=/comment/92/
        next = request.GET.get('next', None)
        if notification.recipient == request.user:
            notification.read = True
            notification.save()
            if next is not None:
                return HttpResponseRedirect(next)
            else:
                return redirect("notifications_all")
        else:
            raise Http404
    except:
        return redirect("notifications_all")

@login_required
def get_notifications_ajax(request):
    """
    It gets notification for particular user through ajax post call.
    As a result it returns notifications and its count number
    """
    username = request.user.username,
    notifications = Notification.objects.all_for_user(request.user).recent()
    if request.is_ajax() and request.method == "POST":
        notifications = Notification.objects.all_for_user(request.user).recent()
        print("username", request.user.username)
        count = notifications.count()
        notes = []
        for note in notifications:
            notes.append(str(note.get_link))
        data = {
                "notifications": notes,
                "count": count, # count var will be usefull to dermine if we have any notifications
                "username": username,
        }
        json_data = json.dumps(data)
        # json format for java script processing
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404
