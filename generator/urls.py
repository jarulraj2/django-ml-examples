from django.urls import path
from .views import resume_builder

urlpatterns = [
    path('', resume_builder, name='resume_builder'),
]
