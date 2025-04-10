from django.contrib import admin
from django.urls import path, include

# fmt: off
urlpatterns = [
    path("admin/", admin.site.urls), 
    path("api/v1/", include("travel.urls")),
    path("api/v1/auth/", include("accounts.urls")),
]
