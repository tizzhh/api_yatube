from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import PostView

router = routers.DefaultRouter()
router.register(r'posts', PostView)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
