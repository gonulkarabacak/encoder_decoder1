from django.urls import path
from . import views

urlpatterns = [
    path('', views.encode_text, name='encode_text'),
    path('decode/', views.decode_text, name='decode_text'),
]
