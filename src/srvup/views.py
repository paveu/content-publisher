# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.shortcuts import render
# from django.utils.safestring import mark_safe
# from django.http.response import HttpResponseRedirect

# ######## Accounts #####
from accounts.forms import RegisterForm, LoginForm
# from accounts.models import MyUser
########################
from videos.models import Video, Category
from analytics.signals import page_view
from analytics.models import PageView
from comments.models import Comment
# @login_required(login_url='/enroll/login/')


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
