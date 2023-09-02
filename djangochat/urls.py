from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    path('rooms/', include('room.urls')),
    path('admin/', admin.site.urls),
]


# Custom 404 handler for handling url errors
handler404 = 'core.views.custom_404'
