from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from pytils.translit import slugify as cyrillic_slugify 

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Имя тега")
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название статьи")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL (Слаг)")
    description = models.TextField(max_length=1000, verbose_name="Краткое описание статьи")
    text = models.TextField(verbose_name="Текст статьи")
    image = models.ImageField(verbose_name="Изображение статьи")
    tags = models.ManyToManyField(Tag, related_name="articles", blank=True, verbose_name="Теги статьи")
    is_active = models.BooleanField(default=True, verbose_name="Отображается на сайте")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = "Статья в блоге"
        verbose_name_plural = "Статьи в блоге"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = cyrillic_slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title