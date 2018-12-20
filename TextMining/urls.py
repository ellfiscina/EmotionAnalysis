from django.urls import path

from . import views

app_name = 'TextMining'

urlpatterns = [
    path('', views.index, name='index'),
    path('word/', views.word, name='word'),
    path('emotion/', views.emotion, name='emotion'),
]
