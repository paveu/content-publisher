# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.shortcuts import render
# from django.utils.safestring import mark_safe
# from django.http.response import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response as RestResponse
from rest_framework.reverse import reverse as api_reverse
# ######## Accounts #####
from accounts.forms import RegisterForm, LoginForm
# from accounts.models import MyUser
########################
from videos.models import Video, Category
from analytics.signals import page_view
from analytics.models import PageView
from comments.models import Comment

@api_view(["GET"])
def api_home_abc(request):
    data = {
        "projects": {
            "count": Category.objects.all().count(),
            "url": api_reverse("category_list_api"),

        },
        "comments": {
            "count": Comment.objects.all().count(),
            "url": api_reverse("comment_list_api"),
            },
    }
    return RestResponse(data)


def home(request):
    page_view.send(request.user,
                   page_path=request.get_full_path()
                   )
    if request.user.is_authenticated():
        page_view_obj = request.user.pageview_set.get_videos()[:5]
        recent_videos = []
        for item in page_view_obj:
            if item.primary_object not in recent_videos:
                recent_videos.append(item.primary_object)
        recent_comments = Comment.objects.recent()

        # top items
        video_type = ContentType.objects.get_for_model(Video)
        popular_videos_list = PageView.objects.filter(primary_content_type=video_type).values('primary_object_id').annotate(the_count=Count('primary_object_id')).order_by('-the_count')[:4]
        # print "popular_videos_list", popular_videos_list

        popular_videos = {}

        for item in popular_videos_list:
            the_count = None
            new_video = Video.objects.get(id=item['primary_object_id'])
            if new_video.id == item['primary_object_id']:
                the_count = item['the_count']
            popular_videos[new_video] = the_count

        # one item
        PageView.objects.filter(primary_content_type=video_type, primary_object_id=2)
        context = {"recent_videos": recent_videos,
                   "recent_comments": recent_comments,
                   "popular_videos": popular_videos,
                   }
        template = "home_logged_in.html"
    else:
        featured_categories = Category.objects.get_featured()
        featured_videos = Video.objects.get_featured()
        login_form = LoginForm()
        register_form = RegisterForm()
        context = {"register_form": register_form,
                   "login_form": login_form,
                   "featured_videos": featured_videos,
                   "featured_categories": featured_categories,
                   }
        template = "accounts/home_visitor.html"
    return render(request, template, context)


def jquery_test_view(request):
    return render(request, "jquery_test/view_temp.html", {})


# @login_required(login_url='/staff/login/')
# def staff_home(request):
#     context = {
#                }
#     return render(request, "home.html", context)

# def home(request):
#     print(request.user)
#     if request.user.is_authenticated():
#         name = "Justin"
#         videos = Video.objects.all()
#         embeds = []
#         for vid in videos:
#             code = mark_safe(vid.embed_code)
#             embeds.append("%s" % code)
#         context = {"the_name": name,
#                    "number": videos.count(),
#                    "videos": videos,
#                    "embeds": embeds,
#                    }
#         return render(request, "home.html", context)
#     else:
#         return HttpResponseRedirect("/login/")
