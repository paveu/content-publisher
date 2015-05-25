from django.core.urlresolvers import reverse 
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http.response import Http404, HttpResponseRedirect

# Create your views here.
from .models import Video, Category, TaggedItem
from analytics.signals import page_view 
########## Commments stuff ####
from comments.forms import CommentForm
from comments.models import Comment
#################################

from .serializers import CategorySerializer, VideoSerializer

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import serializers, viewsets, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class VideoDetailAPIView(generics.RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cat_slug = self.kwargs["cat_slug"]
        vid_slug = self.kwargs["vid_slug"]
        category = get_object_or_404(Category, slug=cat_slug)
        obj = get_object_or_404(Video, category=category, slug=vid_slug)
        return obj


class CategoryListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    paginate_by = 10


class CategoryDetailAPIView(generics.RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        slug = self.kwargs["slug"]
        obj = get_object_or_404(Category, slug=slug)
        return obj

#@login_required
def video_detail(request, cat_slug, vid_slug):
    cat = get_object_or_404(Category, slug=cat_slug)
    obj = get_object_or_404(Video, slug=vid_slug, category=cat)
    page_view.send(
                   request.user, 
                   page_path=request.get_full_path(), 
                   primary_obj=obj, 
                   secondary_obj=cat
                   )
    if request.user.is_authenticated() or obj.has_preview:
        try:
            is_member = request.user.is_member
        except:
            is_member = None
        if is_member or obj.has_preview:
            comment_form = CommentForm()
            comments = obj.comment_set.all()
#             for c in comments:
#                 print "!!!!comment!!!: %s !!!!get_children!!!: %s" % (c, c.get_children())
            #     content_type = ContentType.objects.get_for_model(obj)
            #     tags = TaggedItem.objects.filter(content_type=content_type, object_id=obj.id)
            #     print "obj.tags.all()", obj.tags.all()
            #     print "tags", tags
            #     print "content_type", content_type
    
        #         comments = Comment.objects.filter(video=obj)
            context = {
                       "obj":obj,
                       "comments":comments,
                       "comment_form": comment_form,
                       }
            return render(request, "videos/video_detail.html", context )
        else:
            next_url = obj.get_absolute_url()
            return HttpResponseRedirect("%s?next=%s" % (reverse('account_upgrade'), next_url))
    else:
        # upgrade account
        next_url = obj.get_absolute_url()
        return HttpResponseRedirect("%s?next=%s" % (reverse('login'), next_url))

def category_list(request):
    queryset = Category.objects.all()
#     print "queryset", queryset
    context = {
               "queryset": queryset
               }
    return render(request, "videos/category_list.html", context)

# @login_required
def category_detail(request, cat_slug):
#     print request.get_full_path() # /projects/cat-1/
#     path =  request.get_full_path()
#     comments = Comment.objects.filter(path=path)
#     print "comments", comments
    obj = get_object_or_404(Category, slug=cat_slug)
    queryset = obj.video_set.all()
    page_view.send(
                   request.user, 
                   page_path=request.get_full_path(), 
                   primary_obj=obj, 
                   )
    return render(request, "videos/video_list.html", {
                                                      "obj": obj, 
                                                      "queryset": queryset, 
    #                                                  "comments": comments
                                                      })


    
# def video_edit(request):
#     return render(request, "videos/video_single.html", {})
# 
# def video_create(request):
#     return render(request, "videos/video_single.html", {})
