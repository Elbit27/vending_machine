from rest_framework import generics
from rest_framework.response import Response
from .models import Purchase
from . import serializers

class BuyAPI(generics.CreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer

    def post(self, request, *args, **kwargs):
        # Используем сериализатор для валидации и сохранения данных
        serializer = self.get_serializer(data=request.data)

        # Проверяем, валиден ли сериализатор
        if serializer.is_valid():
            purchase = serializer.save()
            response_data = {
                "message": f"Вы купили {purchase.product.name} за {purchase.product.price} сом, "
                           f"вот ваша сдача: {purchase.change} сом."
            }
            return Response(response_data, status=201)
        return Response(serializer.errors, status=400)
