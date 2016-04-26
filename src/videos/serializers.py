from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import serializers, viewsets, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Video, Category
from comments.serializers import CommentSerializer
from rest_framework.reverse import reverse


class VideoUrlHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    """
    VideoUrlHyperlinkedIdentityField class refers generic view 'VideoDetailAPIView' 
    that exists in videos/views.py 
    """
    def get_url(self, obj, view_name, request, format):
        kwargs = {
            'cat_slug': obj.category.slug,
            "vid_slug": obj.slug
        }
        return reverse(view_name,
                       kwargs=kwargs,
                       request=request,
                       format=format)


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    """
    Main class for serializing Video model
    """
    # customized API getting a link to Video instance. it uses VideoUrlHyperlinkedIdentityField class.
    url = VideoUrlHyperlinkedIdentityField("video_detail_api")

    # adding additional category field to Video Serializer
    category_url = serializers.CharField(source='category.get_absolute_url', read_only=True)
    
    # Taking all comments related to Video instance and putting it into VideoSerializer model
    comment_set = CommentSerializer(many=True, read_only=True)

    # it serializes entire model into Video Serializers, it prints out all fields in Category model
    # category = CategorySerializer(many=False, read_only=True)

    # category_title = serializers.CharField(source='category.title', read_only=True)
    # category_image = serializers.CharField(source='category.get_image_url', read_only=True)
    
    # PrimaryKeyRelatedField is needed for getting an access to related field which is in this case Category Model
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    
    class Meta:
        model = Video
        fields = ['url', # it's URL for API itself not model's API
                  'id',
                  'slug',
                  'title',
                  'order',
                  'embed_code',
                  'free_preview',
                  'description',
                  'timestamp',
                #   'category', # taken from serialized Category class
                  # 'category_title',
                  # 'category_image',
                  'category_url',
                  'comment_set', # _set will show any comments related to pointed video
                  ]

### VideoViewSet is depricated. Take a look at generic views in videos/views.py
class VideoViewSet(viewsets.ModelViewSet):
    """
    Setting up VideoSet for Video Model based on previous created
    Video serializer
    """
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # it's taking all objects from Video model and serializing it
    # based on VideoSerializer structure
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """
    Main class for serializing Category model
    """
    # url objects calls 'category_detail_api' along with 'slug' argument to get
    # Category instance. It uses reverse 'category_detail_api' which exists in urls.py
    url = serializers.HyperlinkedIdentityField('category_detail_api',
                                               lookup_field='slug')

    # it serializes entire Video model into Category Serializer. it prints out all fields from Videp model
    video_set = VideoSerializer(many=True)
    
    class Meta:
        model = Category
        fields = ['url',  # it's project Category REST API
                  'id',
                  'slug',
                  'title',
                  'description',
                  'image',
                  'video_set',
                  ]

### CategoryViewSet is depricated. Take a look at generic views in videos/views.py
class CategoryViewSet(viewsets.ModelViewSet):
    """
    Setting up CategoryViewSet for Category Model based on previous created
    Category serializer
    """
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
