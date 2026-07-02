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

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Наименование бренда")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(upload_to="brand/gallery", verbose_name="Изображение")
    
    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"
        ordering = ['name']
    
    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Наименование товара"
    )
    sku = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="Артикул товара"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name="Категория товара"
    )
    
    description = models.TextField(verbose_name="Описание товара")
    
    product_length = models.DecimalField(
        decimal_places=2, 
        max_digits=6, 
        blank=True, 
        null=True, 
        verbose_name="Длина товара (см)"
    )
    product_width = models.DecimalField(
        decimal_places=2, 
        max_digits=6, 
        blank=True, 
        null=True, 
        verbose_name="Ширина товара (см)"
    )
    product_height = models.DecimalField(
        decimal_places=2, 
        max_digits=6, 
        blank=True, 
        null=True, 
        verbose_name="Высота товара (см)"
    )
    product_weight = models.DecimalField(
        decimal_places=2, 
        max_digits=6, 
        blank=True, 
        null=True, 
        verbose_name="Вес товара (см)"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    
    