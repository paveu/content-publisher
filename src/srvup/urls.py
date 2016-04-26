from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework import routers
from videos.serializers import VideoViewSet, CategoryViewSet
from comments.serializers import CommentViewSet
from comments.views import CommentAPICreateView, CommentDetailAPIView, CommentListAPIView
from videos.views import CategoryListAPIView, CategoryDetailAPIView, VideoDetailAPIView

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'videos', VideoViewSet)

urlpatterns = patterns('',
    # default API router
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    # in order to get an auth token we need to make curl reqeust (it uses django-rest-framework-jwt/)
    # curl -X POST -d "username=admin&password=abc123" http://localhost:8000/api-token-auth/
    # to get the access with a token: curl -H "Authorization: JWT <your_token>" http://localhost:8000/protected-url/
    url(r'^api/auth/token/$', 'rest_framework_jwt.views.obtain_jwt_token'),

    # new API will look more like project urls so I'm gonna mark it as api2
    url(r'^api2/$', 'srvup.views.new_api_home', name='api_home'),
    # Lists all categories we have
    url(r'^api2/categories/$', CategoryListAPIView.as_view(), name='category_list_api'),
    url(r'^api2/categories/(?P<slug>[\w-]+)/$', CategoryDetailAPIView.as_view(), name='category_detail_api'),
    url(r'^api2/categories/(?P<cat_slug>[\w-]+)/(?P<vid_slug>[\w-]+)/$', VideoDetailAPIView.as_view(), name='video_detail_api'),
    url(r'^api2/comment/$', CommentListAPIView.as_view(), name='comment_list_api'),
    url(r'^api2/comment/create/$', CommentAPICreateView.as_view(), name='comment_create_api'),
    url(r'^api2/comment/(?P<id>\d+)/$', CommentDetailAPIView.as_view(), name='comment_detail_api'),
    url(r'^jquery-test/$', 'srvup.views.jquery_test_view'),

    # Project main navigation map
    url(r'^$', 'srvup.views.home', name='home'),
    url(r'^contact_us/$', TemplateView.as_view(template_name='company/contact_us.html'), name='contact_us'),
    url(r'^categories/$', 'videos.views.category_list', name='categories'),
    url(r'^categories/(?P<cat_slug>[\w-]+)/$', 'videos.views.category_detail', name='cat_detail'),
    url(r'^categories/(?P<cat_slug>[\w-]+)/(?P<vid_slug>[\w-]+)/$', 'videos.views.video_detail', name='video_detail'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# enrollment
urlpatterns += patterns('billing.views',
    url(r'^upgrade/$', 'upgrade', name='account_upgrade'),
    url(r'^billing/$', 'billing_history', name='billing_history'),
    url(r'^billing/cancel$', 'cancel_subscription', name='cancel_subscription'),
)

# auth login/logout/register
urlpatterns += patterns('accounts.views',
    url(r'^accounts/account/$', 'account_home', name='account_home'),
    url(r'^accounts/login/$', 'auth_login', name='login'),
    url(r'^accounts/logout/$', 'auth_logout', name='logout'),
    url(r'^accounts/register/$', 'auth_register', name='register'),
)

# Comment Thread
urlpatterns += patterns('comments.views',
    url(r'^comments/(?P<id>\d+)/$', 'comment_thread', name='comment_thread'),
    url(r'^comments/create/$', 'comment_create_view', name='comment_create'),
)

# Notifications Thread
urlpatterns += patterns('notifications.views',
    url(r'^notifications/$', 'all', name='notifications_all'),
    url(r'^notifications/ajax/$', 'get_notifications_ajax', name='get_notifications_ajax'),
    url(r'^notifications/read/(?P<id>\d+)/$', 'read', name='notifications_read'),
)
