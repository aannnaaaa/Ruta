from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.shortcuts import render


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_pages.urls')),
    path('profile/', include('profiles.urls')),
    path('blog/', include('blog.urls')),
    path('routes/', include('routes.urls')),
    path('', include('about_page.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)