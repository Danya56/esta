from django.shortcuts import render
from django.urls import reverse
from django.middleware.csrf import get_token
from .models import Slide, Sertificate, CallbackRequest, Company
from .services import send_client_email
from django.http import HttpResponse, HttpRequest
from django_ratelimit.decorators import ratelimit
import json 

def index(request: HttpRequest) -> HttpResponse:
    slides = Slide.objects.filter(is_active=True)
    certificates = Sertificate.objects.filter(is_active=True)
    context = {
        'slides': slides.reverse(),
        'certificates': certificates.reverse(),
    }
    return render(request, 'main/index.html', context)

def calc_request(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        area = float(request.POST.get('area', 0))
        height = float(request.POST.get('height', 0))
        fuel = request.POST.get('fuel')
        object_type = request.POST.get('object_type', 'Нет данных')
        montage = request.POST.get('montage', 'Нет данных')
        volume = area * height
        estimated_power = round(volume / 30, 1)
        
        if estimated_power < 50: estimated_power = 50
        if estimated_power > 1000: estimated_power = 1000

        csrf_token_value = get_token(request)

        html_response = f"""
        <div class="bg-orange-50 border border-orange-200 rounded p-4 text-center">
            <p class="text-sm text-gray-600">Ориентировочная мощность для вашего объекта:</p>
            <p class="text-2xl font-black text-esta-accent mt-1">{estimated_power} кВт</p>
            <p class="text-xs text-gray-500 mt-2">Оставьте контактные данные, инженер свяжется для точного теплорасчета и подбора модели.</p>
            <form class="flex flex-col mt-3 max-w-xs mx-auto flex gap-2" hx-post="{reverse('callback_submit')}" >
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token_value}">
                <input type="hidden" name="area" value="{area}">
                <input type="hidden" name="height" value="{height}">
                <input type="hidden" name="fuel" value="{fuel}">
                <input type="hidden" name="estimated_power" value="{estimated_power}">
                <input type="hidden" name="object_type" value="{object_type}">
                <input type="hidden" name="montage" value="{montage}">

                <input type="text" name="name" placeholder="Имя" class="border border-gray-300 rounded px-3 py-1.5 text-sm w-full focus:outline-orange-500" required>
                <input type="email" name="email" placeholder="Email" class="border border-gray-300 rounded px-3 py-1.5 text-sm w-full focus:outline-orange-500" required>
                <input type="tel" name="phone" placeholder="+7 (___) ___-__-__" class="border border-gray-300 rounded px-3 py-1.5 text-sm w-full focus:outline-orange-500" required>
                <div x-data="{{agree: false}}" class="flex pt-2 lg:pt-0 flex-col relative">
                    <label class="flex gap-x-1 lg:gap-x-2 items-center text-sm">
                        <input type="checkbox" x-model="agree"><span class="cursor-pointer underline text-left" @click="$dispatch('open-personal-document')">Согласие на обработку персональных данных</span>
                    </label>
                    <button type="submit"
                            :disabled="!agree"
                            class="flex gap-x-2 items-center justify-center bg-esta-accent text-white px-4 py-4 rounded text-sm font-bold hover:bg-esta-accent-hover transition mt-6 disabled:opacity-40 disabled:cursor-not-allowed">
                        Оставить заявку
                    </button>
                    <div x-show="!agree" 
                        class="text-xs absolute -bottom-4">
                        *Сначала примите согласие
                    </div>
                </div>
                <div id="loading-spinner" class="htmx-indicator flex items-center justify-center gap-2 mt-4 text-gray-600">
                    <svg class="animate-spin h-5 w-5 text-esta-accent" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>Отправляем данные, пожалуйста, подождите...</span>
                </div>
            </form>
        </div>
        """
        return HttpResponse(html_response)
    
    return HttpResponse("Метод не разрешен", status=405)

@ratelimit(key='ip', rate='5/m', method='POST', block=False)
def callback_submit(request: HttpRequest) -> HttpResponse:

    was_limited = getattr(request, 'limited', False)
    if was_limited:
        response = HttpResponse("Слишком много запросов. Попробуйте позже.", status=429)
        response['HX-Trigger'] = json.dumps({
            "show-toast": {"text": "Пожалуйста, подождите минуту перед повторной отправкой."}
        })
        return response
    
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        area_val = request.POST.get('area', '')
        height_val = request.POST.get('height', '')
        fuel_val = request.POST.get('fuel', '')
        montage_val = request.POST.get('montage', '')
        build_val = request.POST.get('object_type', '')
        power_val = request.POST.get('estimated_power', '')
        user_comment = request.POST.get('comment', '')

        if not name or not phone:
            return HttpResponse("Пожалуйста, заполните обязательные поля", status=400)

        fuel_mapping = {
            'gas': 'газ',
            'diesel': 'дизель',
            'oil': 'отработанное масло',
            'solid': 'твердое',
        }

        montage_mapping = {
            'stacionar': 'Стационарный',
            'podvesnoy': 'Подвесной'
        }

        build_mapping = {
            'warehouse': 'Склад',
            'car_services': 'Автосервис / СТО',
            'manufacture': 'Производственный цех',
            'agriculture': 'Сельское хозяйство',
            'other': 'Другое'
        }

        lead_info = f"""
            Данные с калькулятора:
            - Тип объекта: {build_mapping.get(build_val, 'Нет данных')}
            - Площадь: {area_val} кв.м.
            - Высота потолков: {height_val} м
            - Тип топлива: {fuel_mapping.get(fuel_val, 'Нет данных')}
            - Тип монтажа: {montage_mapping.get(montage_val, 'Нет данных')}
            - Требуемая мощность: {power_val} кВт
            """

        if area_val:
            user_comment = f"{user_comment}\n{lead_info}".strip()

        CallbackRequest.objects.create(name=name, phone=phone, email=email, comment=user_comment)

        response = HttpResponse(status=200)
        
        if area_val:
            response = HttpResponse("""
                <div class="flex flex-wrap bg-green-600 text-white py-3 rounded-lg shadow-2xl items-center justify-center gap-x-2">
                    <p>Спасибо за заявку!</p>
                    <p>Мы скоро свяжемся с вами.</p>
                </div>
            """)
        else:
            response = HttpResponse(status=204)

        client_data = {
                'name': name,
                'phone': phone,
                'email': email,
                'message': user_comment
            }
        
        send_client_email(client_data)

        response['HX-Trigger'] = json.dumps({
            "show-toast": {"text": "Спасибо, мы скоро вам перезвоним!"}
        })
        return response
    
    return HttpResponse("Метод не разрешен", status=405)

def about_index(request: HttpRequest) -> HttpResponse:
    info_company = Company.objects.first()

    context = {
     'info_company': info_company,
    }
    
    return render(request, 'about/index.html', context)

def delivery_index(request: HttpRequest) -> HttpResponse:
    return render(request, 'delivery/index.html')