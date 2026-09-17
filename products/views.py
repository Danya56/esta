# pyright: reportAttributeAccessIssue=false
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Prefetch
from .models import Attribute, Category, Product, Brand, ProductValue, CategoryAttribute

def get_attributes_by_category(request):
    category_id = request.GET.get('category_id')
    attributes = Attribute.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(attributes), safe=False)

def catalog(request):
    categories = Category.objects.filter(parent__isnull=True)
    return render(request, 'catalog/index.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)

    # Все товары этой категории
    products = (
        Product.objects
        .filter(category=category)
        .select_related('brand')
    )

    # Все бренды, у которых есть товары в этой категории
    brands = (
        Brand.objects
        .filter(products__category=category)
        .distinct()
    )

    # Все верхнеуровневые категории
    categories = (
        Category.objects
        .filter(parent__isnull=True)
        .prefetch_related('children')
    )

    # ---------------------------------------------------------
    # Получаем значения характеристик товаров
    # ---------------------------------------------------------

    category_attrs = list(
        CategoryAttribute.objects
        .filter(category=category)
        .select_related('attribute')
    )

    product_ids = [p.id for p in products]

    values_map = {}
    used_attr_ids = set()
    if product_ids:
        for pv in ProductValue.objects.filter(product_id__in=product_ids).only(
            'product_id', 'attribute_id', 'value'
        ):
            values_map.setdefault(pv.product_id, {})[pv.attribute_id] = pv.value
            if pv.value and pv.value.strip():
                used_attr_ids.add(pv.attribute_id)

    category_attrs = [
        ca for ca in CategoryAttribute.objects
        .filter(category=category)
        .select_related('attribute')
        if ca.pk in used_attr_ids
    ][:5]

    products_data = [
        {
            'obj': p,
            'cells': [
                (attr, values_map.get(p.id, {}).get(attr.id, ''))
                for attr in category_attrs
            ],
        }
        for p in products
    ]

    # ---------------------------------------------------------
    # Группируем товары по брендам
    # ---------------------------------------------------------

    brands_data = []

    for brand in brands:
        brand_products = [
            product_data
            for product_data in products_data
            if product_data['obj'].brand_id == brand.id
        ]

        if brand_products:
            brands_data.append({
                'obj': brand,
                'products': brand_products,
            })

    context = {
        'category': category,
        'categories': categories,
        'category_attrs': category_attrs,

        'products_data': products_data,
        'brands': brands,

        # Новая структура
        'brands_data': brands_data,
    }

    return render(
        request,
        'catalog/category_detail.html',
        context
    )

def brand_detail(request, category_slug, brand_slug):
    category = get_object_or_404(Category, slug=category_slug)
    brand = get_object_or_404(Brand, slug=brand_slug)

    products = list(
        Product.objects
        .filter(category=category, brand=brand)
        .select_related('brand')
    )

    categories = (
        Category.objects
        .filter(parent__isnull=True)
        .prefetch_related('children')
    )

    category_attrs = list(
        CategoryAttribute.objects
        .filter(category=category)
        .select_related('attribute')
    )

    product_ids = [p.id for p in products]

    values_map = {}
    used_attr_ids = set()
    if product_ids:
        for pv in ProductValue.objects.filter(product_id__in=product_ids).only(
            'product_id', 'attribute_id', 'value'
        ):
            values_map.setdefault(pv.product_id, {})[pv.attribute_id] = pv.value
            if pv.value and pv.value.strip():
                used_attr_ids.add(pv.attribute_id)

    category_attrs = [
        ca for ca in CategoryAttribute.objects
        .filter(category=category)
        .select_related('attribute')
        if ca.pk in used_attr_ids
    ][:5]

    products_data = [
        {
            'obj': p,
            'cells': [
                (attr, values_map.get(p.id, {}).get(attr.id, ''))
                for attr in category_attrs
            ],
        }
        for p in products
    ]

    context = {
        'category': category,
        'categories': categories,
        'brand': brand,
        'category_attrs': category_attrs,
        'products_data': products_data,
    }
    return render(request, 'catalog/brand_detail.html', context)

def product_detail(request, slug):
    product = (
        Product.objects
        .select_related('brand', 'category')
        .prefetch_related('images')
        .get(slug=slug)
    )

    category = product.category

    categories = (
        Category.objects
        .filter(parent__isnull=True)
        .prefetch_related('children')
    )

    # все атрибуты категории, отсортированные
    category_attrs = list(
        CategoryAttribute.objects
        .filter(category=category)
        .select_related('attribute')
    )

    # словарь {attr_id: value} для этого товара
    values_by_attr = {
        pv.attribute_id: pv.value
        for pv in ProductValue.objects
        .filter(product=product)
        .only('attribute_id', 'value')
    }

    specs = [
        (attr, values_by_attr[attr.pk])
        for attr in category_attrs
        if values_by_attr.get(attr.pk, '').strip()
    ]

    context = {
        'product': product,
        'categories': categories,
        'category': category,
        'specs': specs,
    }
    return render(request, 'catalog/product_detail.html', context)
