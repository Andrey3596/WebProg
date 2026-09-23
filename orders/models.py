from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    class Role(models.IntegerChoices):
        undefined = 0
        service = 1
        client = 2

    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, null=True, blank=True)
    role = models.IntegerField("Роль", choices=Role, default=Role.undefined)
    
    def __str__(self):
        return self.user.username if self.user else f"Profile {self.id}"


@receiver(post_save, sender=User)
def on_user_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance, role=Profile.Role.undefined)
        
        
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
    image = models.ImageField("Картинка", null=True, upload_to='dish')
    
    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        
    def __str__(self):
        return self.name



class Order(models.Model):
    class Status(models.StringChoices):
            processing = 'В обработке'
            ready = 'Готово'
            completed = 'Завершён'
            cancelled ='Отменён'
    
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    created_at = models.DateField('Дата создания', auto_now_add=True)
    status = models.CharField('Статус',max_length=20,  choices=Status, default='processing')
    total_amount = models.DecimalField('Общая сумма',max_digits=10, decimal_places=2,default=0.00)
    
    def __str__(self):
        return f'Заказ #{self.id} от {self.user.username} ({self.created_at.strftime("%d.%m.%Y")})'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
        
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    dish = models.ForeignKey(Dish,on_delete=models.PROTECT)
    
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField('Цена на момент заказа',max_digits=10,decimal_places=2)

    def __str__(self):
        return f'{self.dish.name} x{self.quantity} (заказ #{self.order.id})'

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'