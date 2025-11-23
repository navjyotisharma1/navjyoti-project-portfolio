from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Serve the main UI (index.html) directly from core app
    path('', include('core.urls')),  # This ensures your homepage works at "/"

    # API endpoints
    path('api/', include('core.urls')),  # Keeps your /api/query/ and /api/upload/
]

# Media file handling (for uploaded PDFs)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
