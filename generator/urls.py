from django.urls import path
from .views import resume_builder,generate_docx

urlpatterns = [
    path('', resume_builder, name='resume_builder'),
    path("generate-docx/", generate_docx, name="generate_docx"),
]
