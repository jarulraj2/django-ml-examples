from django.urls import path
from . import views

app_name = 'imageprocessing'  # Namespace

urlpatterns = [
    path('compress/', views.upload_and_compress_pdf, name='compress_pdf'),
    path('download/<str:filename>/', views.download_compressed_pdf, name='download_compressed_pdf'),
    path('generate/', views.generate_local_ai_image, name='generate_local_ai_image'),
]
