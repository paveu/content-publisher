from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import serializers, viewsets, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Video, Category
from comments.serializers import CommentSerializer
from rest_framework.reverse import reverse


class VideoUrlHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):

        kwargs = {
            'cat_slug': obj.category.slug,
            "vid_slug": obj.slug
        }
        print "kwargs:", kwargs
        return reverse(view_name,
                       kwargs=kwargs,
                       request=request,
                       format=format)


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    url = VideoUrlHyperlinkedIdentityField("video_detail_api")
    # category = CategorySerializer(many=False, read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)
    category_url = serializers.CharField(source='category.get_absolute_url', read_only=True)
    # category_title = serializers.CharField(source='category.title', read_only=True)
    # category_image = serializers.CharField(source='category.get_image_url', read_only=True)
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = Video
        fields = ['url',
                  'id',
                  'slug',
                  'title',
                  'order',
                  'embed_code',
                  'free_preview',
                  'description',
                  'timestamp',
                  # 'category', # taken from serialized Category class
                  # 'category_title',
                  # 'category_image',
                  'category_url',
                  'comment_set', # _set will show any comments related to pointed video
                  ]


class VideoViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


# class CategoryUrlHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
# #     lookup_field = 'slug'
#     def get_url(self, obj, view_name, request, format):
#         kwargs = {
#             'slug': obj.slug,
#         }
#         return reverse(view_name, kwargs=kwargs, request=request, format=format)


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    # url = CategoryUrlHyperlinkedIdentityField(view_name='category_detail_api', lookup_field='slug')
    url = serializers.HyperlinkedIdentityField('category_detail_api',
                                               lookup_field='slug')
    video_set = VideoSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id',
                  'url',
                  'slug',
                  'title',
                  'description',
                  'image',
                  'video_set',
                  ]


class CategoryViewSet(viewsets.ModelViewSet):
    # authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
