from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main_index'),
    path('about/', views.about_index, name="about_index"),
    path('calc-request/', views.calc_request, name='calc_request'),
    path('callback-submit', views.callback_submit, name='callback_submit')
]