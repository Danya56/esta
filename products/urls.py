from django.urls import path
from . import views

urlpatterns = [
    path('get-attributes/', views.get_attributes_by_category, name='get_attributes'),
    path('', views.catalog, name='catalog'),

    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    path('<slug:category_slug>/<slug:brand_slug>/', views.brand_detail, name='brand_detail'),

    path('<slug:slug>/', views.category_detail, name='category_detail'),
]