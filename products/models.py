from typing import Iterable
from django.db import models
from pytils.translit import slugify

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Attribute(models.Model):
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='attributes', 
        verbose_name="Категория"
    )
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('category', 'name')
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"
    
    def __str__(self) -> str:
        return f"{self.category.name} - {self.name}"
    
