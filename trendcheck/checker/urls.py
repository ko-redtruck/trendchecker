from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("<str:tag>/<str:user_name>/<str:post_identifier>",views.check)
]
