from django.urls import path
from . import views

urlpatterns = [
    path("top_districts/", views.TopDistrictsView.as_view(), name="top-districts")
]
