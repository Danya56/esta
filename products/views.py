from django.shortcuts import render
from django.http import JsonResponse
from .models import Attribute

def get_attributes_by_category(request):
    print("Попал сюда")
    category_id = request.GET.get('category_id')
    attributes = Attribute.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(attributes), safe=False)

