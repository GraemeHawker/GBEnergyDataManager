from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_unused_BMUs, name='unused_BMUs')
]
