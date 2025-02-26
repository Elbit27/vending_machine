from rest_framework.viewsets import ModelViewSet
from .models import Product
from . import serializers


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return serializers.ProductCreateUpdateSerializer
        return serializers.ProductSerializer
