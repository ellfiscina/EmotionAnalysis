from django.urls import path

from . import views

app_name = 'TextMining'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('emotion/', views.emotion, name='emotion'),
]
