from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.PositiveIntegerField()

    class Meta:
        db_table = 'products'   # Явное имя таблицы в БД
        verbose_name = 'Product'   # Название в админке (в единственном числе)
        verbose_name_plural = 'Products'   # Название во множественном числе

    def __str__(self):
        return f'|{self.pk}| {self.name} - {self.price} сом (В наличии: {self.amount})'