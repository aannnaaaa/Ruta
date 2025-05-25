from django.urls import path
from . import views

app_name = 'routes'

urlpatterns = [
    path('create/step1/', views.create_route_step1_view, name='create_route_step1'),
    path('create/step2/', views.create_route_step2_view, name='create_route_step2'),
    path('create/step3/', views.create_route_step3_view, name='create_route_step3'),
]