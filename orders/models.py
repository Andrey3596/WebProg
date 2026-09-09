from django.db import models

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
    
    group = models.ForeignKey("Category", on_delete=models.CASCADE, null=True)
    
    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"