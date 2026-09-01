from django.urls import path
from . import views

urlpatterns = [
    path('get-attributes/', views.get_attributes_by_category, name='get_attributes')
]