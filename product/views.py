from rest_framework.viewsets import ModelViewSet
from .models import Product
from . import serializers

from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


class StandardResultPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = StandardResultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ('id', 'name')

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return serializers.ProductCreateUpdateSerializer
        return serializers.ProductSerializer
