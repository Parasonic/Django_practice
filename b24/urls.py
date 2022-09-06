from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('token_validation/', views.token_validation),
    path('thanks/', views.thanks, name='thanks')
]