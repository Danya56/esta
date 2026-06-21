from django.db import models

class Company (models.Model):
    name = models.CharField("Название", max_length=200);
    description = models.TextField("Описание компании");
    image = models.ImageField("Изображение компании", upload_to="company/");

    class Meta:
        verbose_name = "Информация о компании"
        verbose_name_plural = "Информация о компании"

class Slide (models.Model):
    title = models.CharField("Заголовок", max_length=200)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to="porfolio/")
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Слайд портфолио"
        verbose_name_plural = "Слайды портфолио"
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return self.title or f"Слайд №{self.pk}"

class Sertificate(models.Model):
    title = models.CharField("Название", max_length=200, blank=True)
    is_active = models.BooleanField("Активен", default=True)
    image = models.ImageField("Изображение", upload_to="certificate/")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return self.title or f"Сертификат №{self.pk}"

class CallbackRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.CharField(max_length=60, verbose_name='Email')
    comment = models.TextField(max_length=1000, verbose_name="Комментарий клиента", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заявки')
    is_processed = models.BooleanField(default=False, verbose_name='Обработано')
    
    class Meta:
        verbose_name = 'Заявка с сайта'
        verbose_name_plural = 'Заявки с сайта'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.phone}"