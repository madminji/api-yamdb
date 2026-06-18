from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views


router_v1 = DefaultRouter()
router_v1.register('categories', views.CategoryViewSet, basename='category')
router_v1.register('genres', views.GenreViewSet, basename='genre')
router_v1.register('titles', views.TitleViewSet, basename='title')

api_v1_patterns = [
    path('', include(router_v1.urls)),
    path('auth/signup/', views.signup, name='signup'),
    path('auth/token/', views.get_token, name='get_token'),
]

urlpatterns = [
    path('v1/', include(api_v1_patterns)),
]
