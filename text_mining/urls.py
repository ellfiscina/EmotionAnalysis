from django.urls import path

from . import views

app_name = 'text_mining'

urlpatterns = [
    path('', views.index, name='index'),
    path('word/', views.word, name='word'),
    path('emotion/', views.emotion, name='emotion'),
    path('context/', views.context, name='context'),
]
