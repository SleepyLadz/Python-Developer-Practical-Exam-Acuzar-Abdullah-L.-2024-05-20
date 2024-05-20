from .views import CarView
from django.urls import path

urlpatterns = [
    path('', CarView.get_car, name='car_list'),
    path('get_car', CarView.get_car, name='car_list'),
    path('post_switch_car/', CarView.post_switch_car, name='post_switch_car'),
    path('sorting_blue_cars/', CarView.sorting_blue_cars, name='sorting_blue_cars'),
    path('sorting_red_cars/', CarView.sorting_red_cars, name='sorting_red_cars'),
]
