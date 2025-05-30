from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('supervised/', views.supervised_view, name='supervised'),
    path('unsupervised/', views.unsupervised_view, name='unsupervised'),
    path('reinforcement/', views.reinforcement_view, name='reinforcement'),
]
