from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.TextField("Название категории")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        
    def __str__(self) -> str:
        return self.name
    

class Dish(models.Model):
    name = models.TextField("Название блюда")
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True)
    
    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        
    def __str__(self):
        return self.name



class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'В обработке'),
        ('ready', 'Готово'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
    ]

    
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    
    created_at = models.DateField('Дата создания', auto_now_add=True)
    
    status = models.CharField('Статус',max_length=20,  choices=STATUS_CHOICES, default='processing')
    
    total_amount = models.DecimalField('Общая сумма',max_digits=10, decimal_places=2,default=0.00)

    def __str__(self):
        return f'Заказ #{self.id} от {self.user.username} ({self.created_at.strftime("%d.%m.%Y")})'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
        
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish,on_delete=models.PROTECT)
    
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField('Цена на момент заказа',max_digits=10,decimal_places=2)

    def __str__(self):
        return f'{self.dish.name} x{self.quantity} (заказ #{self.order.id})'

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'