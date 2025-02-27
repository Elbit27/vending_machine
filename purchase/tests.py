from django.test import TestCase
from django.core.exceptions import ValidationError
from product.models import Product
from purchase.models import Purchase
from rest_framework.test import APITestCase
from rest_framework import status

#---------------------------------------------------------------------------------------------------------------
# Тесты для административной панели и ручного взаимодействия с БД
class PurchaseTestCase(TestCase):
    def setUp(self):
        """Создаем тестовый товар"""
        self.product = Product.objects.create(name="Coca-Cola", price=50.00, amount=5)

    def test_successful_purchase(self):
        """Тест успешной покупки"""
        purchase = Purchase.objects.create(product=self.product, pay=100.00)
        self.product.refresh_from_db()  # Обновляем объект из БД

        self.assertEqual(purchase.change, 50.00)  # Проверяем сдачу
        self.assertEqual(self.product.amount, 4)  # Проверяем, что amount уменьшился на 1

    def test_insufficient_funds(self):
        """Тест ошибки при недостатке средств"""
        with self.assertRaises(ValidationError) as context:
            Purchase.objects.create(product=self.product, pay=40.00)

        self.assertIn("Недостаточно средств", str(context.exception))

    def test_out_of_stock(self):
        """Тест ошибки, когда товара нет в наличии"""
        self.product.amount = 0
        self.product.save()

        with self.assertRaises(ValidationError) as context:
            Purchase.objects.create(product=self.product, pay=100.00)

        self.assertIn("Товар 'Coca-Cola' закончился", str(context.exception))

    def test_correct_change(self):
        """Тест корректности сдачи"""
        purchase = Purchase.objects.create(product=self.product, pay=75.00)
        self.assertEqual(purchase.change, 25.00)

#---------------------------------------------------------------------------------------------------------------
# Тесты для API
class PurchaseAPITestCase(APITestCase):
    def setUp(self):
        """Создаем тестовый товар"""
        self.product = Product.objects.create(name="Coca-Cola", price=50.00, amount=5)
        self.purchase_url = "/buy/"

    def test_successful_purchase(self):
        """Тест успешной покупки"""
        data = {"product": self.product.id, "pay": 100}
        response = self.client.post(self.purchase_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(response.data["message"], "Вы купили Coca-Cola за 50.00 сом, вот ваша сдача: 50.00 сом.")
        self.product.refresh_from_db()
        self.assertEqual(self.product.amount, 4)

    def test_not_enough_money(self):
        """Тест ошибки при недостатке средств"""
        data = {"product": self.product.id, "pay": 10}
        response = self.client.post(self.purchase_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(response.data["non_field_errors"][0], "Недостаточно средств для покупки товара coca-cola. Товар coca-cola стоит 50.00 сом.")

    def test_product_out_of_stock(self):
        """Тест ошибки, когда товара нет в наличии"""
        self.product.amount = 0
        self.product.save()

        data = {"product": self.product.id, "pay": 100}
        response = self.client.post(self.purchase_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(response.data["non_field_errors"][0], "Продукта под именем coca-cola, нет в наличии!.")
