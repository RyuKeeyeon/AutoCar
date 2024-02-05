# control/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('forward/', views.forward, name='forward'),
    path('backward/', views.backward, name='backward'),
]
