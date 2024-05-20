from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from .models import Car
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction


class CarView(View):
    def get_car(request):
        cars = Car.objects.all().order_by('position')
        return render(request, 'car_app/list_cars.html', {'cars': cars})

    def sorting_blue_cars(request):
        if request.method == 'GET':
            blue_cars = Car.objects.filter(color='blue').order_by('position')
            return render(request, 'car_app/blue_cars.html', {'blue_cars': blue_cars})
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)

    def sorting_red_cars(request):
        if request.method == 'GET':
            red_cars = Car.objects.filter(color='red').order_by('position')
            return render(request, 'car_app/red_cars.html', {'red_cars': red_cars})
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)

    @csrf_exempt
    def post_switch_car(request):
        if request.method == 'POST':
            data = request.POST.getlist('car[]')  # Assuming you're sending car IDs in the request

            # Fetch cars ordered by their original positions
            cars = Car.objects.filter(pk__in=data).order_by('position')

            # Update positions sequentially
            with transaction.atomic():
                for new_pos, car_id in enumerate(data, start=1):
                    car = cars.get(pk=car_id)
                    car.position = new_pos
                    car.save()

            return JsonResponse({'message': 'Positions updated successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)

