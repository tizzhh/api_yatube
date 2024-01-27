from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import CommentSerializer, GroupView, PostView

router = routers.DefaultRouter()
router.register(r'posts', PostView)
router.register(r'groups', GroupView)
router.register(
    r'posts/(?P<post_pk>\d+)/comments', CommentSerializer, basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
