from django.shortcuts import render
from rest_framework.generics import (
    ListCreateAPIView,
    DestroyAPIView,
    CreateAPIView,
    ListAPIView,
)
from .models import Nodes, Edges, RouteHistory
from .serializers import (
    NodeSerializer,
    EdgeGetSerializer,
    EdgePostSerializer,
    RouteHistoryCreateSerializer,
    RouteHistoryListSerializer,
)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class NodeListCreateAPIView(ListCreateAPIView):
    queryset = Nodes.objects.all()
    serializer_class = NodeSerializer


class EdgeListCreateAPIView(ListCreateAPIView):
    queryset = Edges.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EdgePostSerializer
        return EdgeGetSerializer


class NodeDestroyAPIView(DestroyAPIView):
    queryset = Nodes.objects.all()
    serializer_class = NodeSerializer


class EdgeDestroyAPIView(DestroyAPIView):
    queryset = Edges.objects.all()
    serializer_class = EdgeGetSerializer


class RouteHistoryCreateAPIView(CreateAPIView):
    queryset = RouteHistory.objects.all()
    serializer_class = RouteHistoryCreateSerializer


class RouteHistoryListAPIView(ListAPIView):
    queryset = RouteHistory.objects.all()
    serializer_class = RouteHistoryListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        "source__name",
        "destination__name",
    ]
    search_fields = ["created_at"]
    pagination_class = PageNumberPagination
    pagination_class.page_size_query_param = "limit"


class RouteHistoryDestoryAPIView(DestroyAPIView):
    queryset = RouteHistory.objects.all()
    serializer_class = RouteHistoryListSerializer
