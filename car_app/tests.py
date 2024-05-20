from django.test import TestCase, Client
from django.urls import reverse
from .models import Car


class CarViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create some car instances
        Car.objects.create(name="Car1", color="blue", position=1)
        Car.objects.create(name="Car2", color="red", position=2)

    def test_get_car(self):
        response = self.client.get(reverse('get_car'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_app/list_cars.html')
        self.assertEqual(len(response.context['cars']), 2)

    def test_sorting_blue_cars(self):
        response = self.client.get(reverse('sorting_blue_cars'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_app/blue_cars.html')
        self.assertEqual(len(response.context['blue_cars']), 1)
        self.assertEqual(response.context['blue_cars'][0].color, 'blue')

    def test_sorting_red_cars(self):
        response = self.client.get(reverse('sorting_red_cars'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_app/red_cars.html')
        self.assertEqual(len(response.context['red_cars']), 1)
        self.assertEqual(response.context['red_cars'][0].color, 'red')

    def test_post_switch_car(self):
        car1 = Car.objects.get(name="Car1")
        car2 = Car.objects.get(name="Car2")
        response = self.client.post(reverse('post_switch_car'), {'car[]': [car2.pk, car1.pk]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Positions updated successfully')

        # Verify the positions have been updated
        car1.refresh_from_db()
        car2.refresh_from_db()
        self.assertEqual(car1.position, 2)
        self.assertEqual(car2.position, 1)

    def test_post_switch_car_invalid_method(self):
        response = self.client.get(reverse('post_switch_car'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid request method')
