from django.db import models
from product.models import Product
from django.core.exceptions import ValidationError

class Purchase(models.Model):
    product = models.ForeignKey(Product,  on_delete=models.CASCADE, related_name='purchases')
    pay = models.DecimalField(max_digits=10, decimal_places=2)
    change = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False)  # Это поле будет хранить сдачу
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'purchase'   # Явное имя таблицы в БД
        verbose_name = 'purchase'   # Название в админке (в единственном числе)
        verbose_name_plural = 'purchases'   # Название во множественном числе


    def save(self, *args, **kwargs):
        """Эта обработка ошибок для админки или для ручной работы в БД"""
        # Проверка, хватает ли денег для оплаты товара
        if self.pay < self.product.price:
            raise ValidationError(f"Недостаточно средств для оплаты товара '{self.product.name}'.")
        if self.product.amount <= 0:
            raise ValidationError(f"Товар '{self.product.name}' закончился.")

        # После успешной покупки, количество товара уменьшаем на 1...
        self.product.amount -= 1
        self.product.save()

        # ...и вычисляем сдачу
        self.change = self.pay - self.product.price
        super(Purchase, self).save(*args, **kwargs)  # Вызываем родительский метод для сохранения объекта

    def __str__(self):
        return f'{self.product.name} - {self.pay} - {self.change}'

