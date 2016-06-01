from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect

from .models import Video, Category
from .permissions import IsMember
from analytics.signals import page_view
from comments.forms import CommentForm

# Rest api
from .serializers import CategorySerializer, VideoSerializer
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class VideoDetailAPIView(generics.RetrieveAPIView):
    """
    new REST view:
    Generic View for Detail Api view in this case for Video entry details
    """
    authentication_classes = [SessionAuthentication, 
                            BasicAuthentication,
                            JSONWebTokenAuthentication
                            ]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    
    # it checks whether user is a member or a video has a free_preview access
    # if don't he/she won't get an accees.
    # IsMember permission is defined in videos/permissions.py file
    permission_classes = [IsMember]

    def get_object(self):
        cat_slug = self.kwargs["cat_slug"]
        vid_slug = self.kwargs["vid_slug"]
        category = get_object_or_404(Category, slug=cat_slug)
        obj = get_object_or_404(Video, category=category, slug=vid_slug)
        return obj


class CategoryListAPIView(generics.ListAPIView):
    """
    new REST view:
    Generic View for Listing out all category instances stored in Category Model
    """
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication,
                              # for token auth
                              JSONWebTokenAuthentication]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    paginate_by = 10 # limited to 10 records on the page


class CategoryDetailAPIView(generics.RetrieveAPIView):
    """
    new REST view:
    Generic View for Detail Api view in this case for Category entry details
    """
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication,
                              # for token auth
                              JSONWebTokenAuthentication]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        slug = self.kwargs["slug"]
        obj = get_object_or_404(Category, slug=slug)
        return obj


def video_detail(request, cat_slug, vid_slug):
    """
    Take a look at videos, check if user has a premium account.
    List free videos if possible.
    """
    cat = get_object_or_404(Category, slug=cat_slug)
    video = get_object_or_404(Video, slug=vid_slug, category=cat)
    
    # Log that video page is viewed for analytics purpose
    page_view.send(request.user,
                   page_path=request.get_full_path(),
                   primary_obj=video,
                   secondary_obj=cat
                   )
    
    if request.user.is_authenticated() or video.has_preview:
        try:
            is_member = request.user.is_member
        except:
            is_member = None
        if is_member or video.has_preview:
            comment_form = CommentForm()
            comments = video.comment_set.all()

            context = {"video": video,
                       "comments": comments,
                       "comment_form": comment_form,
                       }
            return render(request, "videos/video_detail.html", context)
        else:
            # If viewer has no premium account, ask for it
            next_url = video.get_absolute_url()
            return HttpResponseRedirect("%s?next=%s" % (reverse('account_upgrade'), next_url))
    else:
        # If viewer is not logged in ask to log in
        next_url = video.get_absolute_url()
        return HttpResponseRedirect("%s?next=%s" % (reverse('account_login'), next_url))

def category_list(request):
    """
    Get all created categories
    """

    all_cat = Category.objects.all()
    context = {"all_cat": all_cat }
    return render(request, "videos/category_list.html", context)

def category_detail(request, cat_slug):
    """
    Get all videos bound to specific category
    """
    cat = get_object_or_404(Category, slug=cat_slug)
    all_videos = cat.video_set.all()
    page_view.send(request.user,
                   page_path=request.get_full_path(),
                   primary_obj=cat,
                   )
    return render(request, "videos/video_list.html", {"cat": cat,
                                                      "all_videos": all_videos,
                                                      })
