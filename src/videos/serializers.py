from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import routers, serializers, viewsets, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Video, Category
from comments.serializers import CommentSerializer

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = [
                    'id',
                    'url',
                    'slug',
                    'title',
                    'description',
                    'image',
                   ]


class CategoryViewSet(viewsets.ModelViewSet):
#     authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)
#     category_url = serializers.CharField(source='category.get_absolute_url', read_only=True)
#     category_title = serializers.CharField(source='category.title', read_only=True)
#     category_image = serializers.CharField(source='category.get_image_url', read_only=True)
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = Video
        fields = [
                    'id',
                    'url',
                    'title',
                    'embed_code',
                    'share_message',
                    'order',
                    'slug',
                    'timestamp',
                    'category', # taken from serialized Category class
#                     'category_title',
#                     'category_image',
#                     'category_url',
                    'comment_set', # _set will show any comments related to pointed video
                   ]


class VideoViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
