from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, Category, Brand, ProductValue, Attribute, Image

class ProductValueInput(admin.TabularInline):
    model = ProductValue
    extra = 1

class ProductImageInput(admin.TabularInline):
    model = Image
    extra = 1

    readonly_fields = ['image_preview']
    
    @admin.display(description="Изображение")
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 100px; height: auto;" />')
        return mark_safe('<div class="live-preview-box" style="color: #999;">Ожидание файла...</div>')

    class Media:
        js = ('admin/js/image_preview.js',);

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "image_preview")
    readonly_fields = ("image_preview", )

    @admin.display(description="Изображение")
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 100px; height: auto;" />')
        return "Изображения нет"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "brand", "created_at")
    inlines = [ProductValueInput, ProductImageInput]

    class Media:
        js = ('admin/js/product_attributes.js',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)

    @admin.display(description="Изображение")
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} style="width: 100px; height: auto;" />')
        return "Изображения нет"

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('get_attribute_name', 'category')
    list_select_related = ('category',)
    
    @admin.display(description="Имя атрибута")
    def get_attribute_name(self, obj):
        return f"Категория: {obj.category.name} Атрибут: {obj.name}" 

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    

