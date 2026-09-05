from django.urls import path
from .views import (
    NodeListCreateAPIView,
    EdgeListCreateAPIView,
    NodeDestroyAPIView,
    EdgeDestroyAPIView,
    RouteHistoryCreateAPIView,
    RouteHistoryListAPIView,
)

urlpatterns = [
    path("nodes/", NodeListCreateAPIView.as_view()),
    path("nodes/<int:pk>/", NodeDestroyAPIView.as_view()),
    path("edges/", EdgeListCreateAPIView.as_view()),
    path("edges/<int:pk>/", EdgeDestroyAPIView.as_view()),
    path("routes/shortest/", RouteHistoryCreateAPIView.as_view()),
    path("routes/history/", RouteHistoryListAPIView.as_view()),
]
