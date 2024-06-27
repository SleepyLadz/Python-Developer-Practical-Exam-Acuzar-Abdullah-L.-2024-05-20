from django.db.models import When, Case, IntegerField, Value
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

    # @csrf_exempt
    # def post_switch_car(request):
    #     data = request.POST.getlist('car[]')  # Assuming you're sending car IDs in the request
    #
    #     # Update positions sequentially
    #     with transaction.atomic():
    #         for new_pos, car_id in enumerate(data, start=1):
    #             Car.objects.filter(pk=car_id).update(position=new_pos)
    #
    #     return JsonResponse({'message': 'Positions updated successfully'}, status=200)

    @csrf_exempt
    def post_switch_car(request):
        data = request.POST.getlist('car[]')  # List of car IDs in new order

        # Prepare the case conditions to update positions based on the new order
        conditions = []
        for index, car_id in enumerate(data):
            conditions.append(When(pk=car_id, then=Value(index + 1)))

        # Perform the bulk update using Case and When
        with transaction.atomic():
            Car.objects.filter(pk__in=data).update(position=Case(*conditions, output_field=IntegerField()))

        return JsonResponse({'message': 'Positions updated successfully'}, status=200)
