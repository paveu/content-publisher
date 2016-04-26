from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import serializers, viewsets, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from .models import Comment

User = get_user_model()


class CommentVideoUrlHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        # try:
        #     print obj.video.category
        # except AttributeError:
        #     return "BLAD"
        # print "obj:", obj
        video = None
        if obj.is_child:
            try:
                video = obj.parent.video
            except:
                video = None
        else:
            try:
                video = obj.video
            except:
                video = None
        if video:
            kwargs = {
                'cat_slug': video.category.slug,
                "vid_slug": video.slug
            }
            return reverse(view_name,
                           kwargs=kwargs,
                           request=request,
                           format=format)
        else:
            return None


class CommentUpdateSerializer(serializers.ModelSerializer):
    """
    It is serializer for updating a comment. It will be used in generic viewsets
    that is located in comments/views.py -> CommentDetailAPIView()
    """
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id',
                  'user',
                  'text']


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for creating commends. It will be used in comments/views.py ->
    -> CommentAPICreateView() class
    """
    class Meta:
        model = Comment
        fields = ['text',
                  'user',
                  'video',
                  'parent',
                  ]


class ChildCommentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Seperate serializer needed to get replies for parent comment.
    It only lists out replies to parent comment
    """
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Comment
        fields = ['id',
                  'user',
                  'text',
                  ]


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Comment Serializer class. It uses another serializer(ChildCommentSerializer) to get replies comments
    """
    # url objects calls 'comment_detail_api' along with 'id' argument to get
    # Comment instance. It uses reverse 'comment_detail_api' which exists in urls.py
    url = serializers.HyperlinkedIdentityField("comment_detail_api",
                                               lookup_field="id")
    
    # replies object uses serialized method called 'get_replies' to get replies to parent comment
    replies = serializers.SerializerMethodField(read_only=True)
    
    ### Legacy code 
    ### user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user = serializers.CharField(source='user.username', read_only=True)
    
    video = CommentVideoUrlHyperlinkedIdentityField("video_detail_api")

    def get_replies(self, instance):
        # to get replies we can use either: instance.get_children() or 
        # or Comment.objects.filter(parent__pk=instance.pk)
        # alternative: queryset = instance.get_children()
        queryset = Comment.objects.filter(parent__pk=instance.pk)
        # for child comments we gonna create new Serializer -> ChildCommentSerializer
        serializer = ChildCommentSerializer(queryset,
                                            context={"request": instance},
                                            many=True)
        return serializer.data

    class Meta:
        model = Comment
        fields = ['url',
                  'id',
                  # 'parent',
                  'user',
                  'video',
                  'text',
                  'replies',

                  ]


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
