from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import CategoriesAndSizes.views

urlpatterns = [
    path("", CategoriesAndSizes.views.home, name="home"),
    path("files/", include('CategoriesAndSizes.urls')),
    path("accounts/", include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)