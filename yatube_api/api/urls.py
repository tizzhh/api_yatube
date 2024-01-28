from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import CommentSerializer, GroupView, PostView

api_v1_router = routers.DefaultRouter()
api_v1_router.register(r'posts', PostView, basename='posts')
api_v1_router.register(r'groups', GroupView, basename='groups')
api_v1_router.register(
    r'posts/(?P<post_pk>\d+)/comments', CommentSerializer, basename='comments'
)

urlpatterns = [
    path('v1/', include(api_v1_router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
