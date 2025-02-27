from rest_framework import serializers
from .models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

    def validate(self, data):
        product = data.get('product')
        pay = data.get('pay')

        if not product:   # Проверяем, существует ли такой товар
            raise serializers.ValidationError("Продукт не найден!")
        if product.amount == 0:   # Проверяем, есть ли продукт в наличии
            raise serializers.ValidationError(f'Продукта под именем {product.name.lower()}, нет в наличии!.')
        if product.price > pay:   # Проверяем, хватает ли денег на покупку
            raise serializers.ValidationError(f'Недостаточно средств для покупки товара {product.name.lower()}. ' 
                                              f'Товар {product.name.lower()} стоит {product.price} сом.')
        return data

    def create(self, validated_data):
        # Создаем объект Purchase с учетом того, что сумма сдачи будет автоматически вычислена
        purchase = Purchase(**validated_data)
        purchase.change = purchase.pay - purchase.product.price


        purchase.save()
        return purchase
