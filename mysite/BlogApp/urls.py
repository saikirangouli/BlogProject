from django.urls import path
from .views import *
urlpatterns = [
    path('register/',UserRegistrationAPIView.as_view(),name='register'),
    path('login/',LoginAPIView.as_view(),name='login'),
    path('blog/<int:pk>/',Blogupdatedelete.as_view(),name='blog_view')
]