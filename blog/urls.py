from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_page, name='blog'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]