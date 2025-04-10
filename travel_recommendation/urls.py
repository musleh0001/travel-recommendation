from django.contrib import admin
from django.urls import path, include

# fmt: off
urlpatterns = [
    path("admin/", admin.site.urls), 
    path("api/", include("travel.urls"))
]
