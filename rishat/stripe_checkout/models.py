from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=128, verbose_name="Название", blank=False)
    description = models.CharField(max_length=32, verbose_name="Описание", blank=True)
    price = models.FloatField(validators=[MinValueValidator(float('0.0'))], verbose_name="Цена без скидки и налога",
                              blank=False)
    currency = models.CharField(verbose_name="Валюта", max_length=16, choices=[('USD', 'Доллар США'),
                                                                               ('EUR', 'Евро'), ],
                                blank=False)

    def __str__(self):
        return f'{self.pk} - {self.name} - {self.price} {self.currency}'

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'
        ordering = ['-name']


class Tax(models.Model):
    taxation_name = models.CharField(max_length=128, verbose_name="Название", blank=False)
    amount = models.FloatField(validators=[MinValueValidator(float('0.0')), MaxValueValidator(float('1.0'))],
                               verbose_name="Налог",
                               blank=False)

    def __str__(self):
        return f'{self.pk} - {self.taxation_name} - {self.amount}'

    class Meta:
        verbose_name_plural = 'Налоги'
        verbose_name = 'Налог'
        ordering = ['-taxation_name']


class Discount(models.Model):
    discount_name = models.CharField(max_length=128, verbose_name="Название", blank=False)
    amount = models.FloatField(validators=[MinValueValidator(float('0.0')), MaxValueValidator(float('1.0'))],
                               verbose_name="Скидка",
                               blank=False)

    def __str__(self):
        return f'{self.pk} - {self.discount_name} - {self.amount}'

    class Meta:
        verbose_name_plural = 'Скидки'
        verbose_name = 'Скидка'
        ordering = ['-discount_name']


class Order(models.Model):
    date_of_order = models.DateField(verbose_name="Дата заказа", blank=True)
    status = models.CharField(verbose_name="Статус", max_length=128, blank=True)
    currency = models.CharField(verbose_name="Валюта", max_length=16, choices=[('USD', 'Доллар США'),
                                                                               ('EUR', 'Евро'), ],
                                blank=False)
    tax_id = models.ForeignKey('Tax', on_delete=models.SET_NULL, null=True, blank=True)
    discount_id = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.pk} - {self.currency}'

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'


class OrderSet(models.Model):
    order_id: Order = models.ForeignKey('Order', on_delete=models.CASCADE, blank=False)
    item_id: Item = models.ForeignKey('Item', on_delete=models.CASCADE, blank=False)
    amount = models.PositiveIntegerField(verbose_name="Количество", blank=False)

    def save(self, *args, **kwargs):
        if self.order_id.currency != self.item_id.currency:
            raise ValueError("Currency must be equals")
        return super(OrderSet, self).save(*args, **kwargs)

    def __str__(self):
        # TODO optimize queries to db
        return f'{self.order_id} - {self.item_id} - {self.amount}'
