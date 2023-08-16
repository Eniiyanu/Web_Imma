from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('run_spider/', views.run_spider, name='run_spider'),
    path('save_file/', views.save_file, name='save_file'),
]
