from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ml_examples.urls')),
    path('bmi/', include('bmicalculator.urls')), 
    path('game/', include(('game.urls', 'game'), namespace='game')),
    path('resume/', include('generator.urls')),
]
# Serve media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)