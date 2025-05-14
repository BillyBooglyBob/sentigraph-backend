from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/sentiment/", include("sentiment.urls")),
    path("api/auth/", include("useraccount.urls")),
    path("api/admin/", include("adminpanel.urls")),
]
