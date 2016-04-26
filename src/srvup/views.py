from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response as RestResponse
from rest_framework.reverse import reverse as api_reverse

from accounts.forms import RegisterForm, LoginForm
from videos.models import Video, Category
from analytics.signals import page_view
from analytics.models import PageView
from comments.models import Comment

@api_view(["GET"])
def get_api_home(request):
    """
    New way of showing default videos
    """
    data = {
        "categories": {
            "count": Category.objects.all().count(),
            "url": api_reverse("category_list_api"),

        },
        "comments": {
            "count": Comment.objects.all().count(),
            "url": api_reverse("comment_list_api"),
            },
        # "videos": {
        #     "count": Video.objects.all().count(),
        #     "url": api_reverse("video_list_api"),
        #     },
    }
    return RestResponse(data)

def jquery_test_view(request):
    """
    jquery test within same domain
    """
    return render(request, "jquery_test/view_temp.html", {})

def home(request):
    """
    Main view function, it is displayed everytime when a user hits "/" root website
    """
    
    # Log a hit to a website into "page_view" page
    page_view.send(request.user, page_path=request.get_full_path())
    
    # Folowing content will be displayed only for those users who are logged in
    if request.user.is_authenticated():
        
        # Filter five recent added videos to categories taken from all viewed videos
        page_view_obj = request.user.pageview_set.get_videos()[:5]
        recent_videos = []
        for item in page_view_obj:
            if item.primary_object not in recent_videos:
                recent_videos.append(item.primary_object)
        
        # Get 10 recent added comments
        recent_comments = Comment.objects.recent()

        # Get top 5 most viewed videos
        video_type = ContentType.objects.get_for_model(Video)
        popular_videos_list = PageView.objects.filter(primary_content_type=video_type).values('primary_object_id').annotate(the_count=Count('primary_object_id')).order_by('-the_count')[:5]
        # print "popular_videos_list", popular_videos_list # popular_videos_list [{'the_count': 12, 'primary_object_id': 1}, {'the_count': 1, 'primary_object_id': 2}]

        popular_videos = {}

        for item in popular_videos_list:
            the_count = None
            new_video = Video.objects.get(id=item['primary_object_id'])
            if new_video.id == item['primary_object_id']:
                the_count = item['the_count']
            popular_videos[new_video] = the_count

        context = {"recent_videos": recent_videos,
                   "recent_comments": recent_comments,
                   "popular_videos": popular_videos,
                   }
        template = "accounts/home_logged_in.html"
    else:
        latest_vids = Video.objects.order_by('-pk')
        # If visitor is not logged in then:
        featured_categories = Category.objects.get_featured()
        featured_videos = Video.objects.get_featured()
        login_form = LoginForm()
        register_form = RegisterForm()
        context = {
                "latest_vids": latest_vids,
                "register_form": register_form,
                "login_form": login_form,
                "featured_videos": featured_videos,
                "featured_categories": featured_categories,
                   }
        template = "accounts/home_visitor.html"
    return render(request, template, context)

