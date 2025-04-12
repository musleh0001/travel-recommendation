from django.urls import path
from . import views

urlpatterns = [
    path("top_districts/", views.TopDistrictsView.as_view(), name="top-districts"),
    path(
        "recommend_travel/",
        views.RecommendTravelView.as_view(),
        name="recommend-travel",
    ),
]
