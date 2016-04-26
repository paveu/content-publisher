from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, Http404, HttpResponseRedirect, get_object_or_404
from rest_framework import generics, mixins, permissions
# Create your views here.
from notifications.signals import notify
from videos.models import Video
from .models import Comment
from .forms import CommentForm

from .permissions import IsOwnerOrReadOnly
from .serializers import CommentCreateSerializer, CommentUpdateSerializer, CommentSerializer


class CommentListAPIView(generics.ListAPIView):
    """
    It will list out all created comments
    """
    # authentication_classes = [SessionAuthentication, 
    #                             BasicAuthentication,
    #                             JSONWebTokenAuthentication]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    paginate_by = 10


class CommentAPICreateView(generics.CreateAPIView):
    """
    It defines API for creating a comment based on serializer coming from
    comments/serializers.py -> CommentCreateSerializer()
    """
    serializer_class = CommentCreateSerializer


class CommentDetailAPIView(mixins.DestroyModelMixin,
                           mixins.UpdateModelMixin,
                           generics.RetrieveAPIView):
    """
    CommentDetailAPIView will be used to update a comment based on 
    CommentUpdateSerializer() serializer located in comments/serializers.py.
    It will also use customized permission class called "IsOwnerOrReadOnly" that
    is located in comments/permissions.py
    """
    # Comment.objects.all() uses CommentManager which means it will filter out
    # only comments that are parents no child comments included
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer
    
    # comment can be updated/deleted only by the owner of the comment otherwise it is read only
    permission_classes = [IsOwnerOrReadOnly, ]
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        """
        It will filter all comments no matter if it is parent comment or child one
        """
        queryset = Comment.objects.filter(pk__gte=0)
        return queryset

    def put(self, request, *args, **kwargs):
        """
        It allows us to udpate a comment
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        It allows us to delete a comment
        """
        return self.destroy(request, *args, **kwargs)


@login_required
def comment_thread(request, id):
    """
    Get comment thread by providing comment id
    """
    comment = get_object_or_404(Comment, id=id)
    form = CommentForm()
    context = {"form": form,
               "comment": comment
               }
    return render(request, "comments/comment_thread.html", context)


def comment_create_view(request):
    """
    Description will be added soon
    """
    if request.method == "POST" and request.user.is_authenticated():

        parent_id = request.POST.get('parent_id')
        video_id = request.POST.get("video_id")

        # origin_path variable is used only for new comment that doesn't have parent
        origin_path = request.POST.get("origin_path")

        try:
            video = Video.objects.get(id=video_id)
        except:
            video = None

        parent_comment = None

        if parent_id is not None:
            try:
                parent_comment = Comment.objects.get(id=parent_id)
            except:
                parent_comment = None

            if parent_comment is not None and parent_comment.video is not None:
                video = parent_comment.video

        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['comment']
            # parent comment section
            if parent_comment is not None:
                new_comment = Comment.objects.create_comment(user=request.user,
                                                             # path=request.get_full_path(),
                                                             path=parent_comment.get_origin,
                                                             #
                                                             text=comment_text,
                                                             video=video,
                                                             parent=parent_comment
                                                             )
                messages.success(request,
                                 "Thank you for your response",
                                 extra_tags='alert-warning')

                notify.send(request.user,
                            action=new_comment,
                            target=parent_comment,
                            recipient=parent_comment.user,
                            affected_users=parent_comment.get_affected_users(),
                            verb='replied to'
                            )
                return HttpResponseRedirect(parent_comment.get_absolute_url())
            
            # Child comment section
            else:
                new_comment = Comment.objects.create_comment(user=request.user,
                                                             #
                                                             # path=request.get_full_path(),
                                                             path=origin_path,
                                                             #
                                                             text=comment_text,
                                                             video=video,
                                                             )
                # option to send to super user or staff users
                notify.send(
                            request.user,
                            action=new_comment,
                            target=new_comment.video,
                            recipient=request.user,
                            verb='commented on'
                            )
                messages.success(request, "Thank you for the comment.")
                # notify.send(request.user, recipient=request.user, action='new comment')
                return HttpResponseRedirect(new_comment.get_absolute_url())
        else:
            messages.error(request, "There was an error with your comment.")
            return HttpResponseRedirect(origin_path)

    else:
        raise Http404
