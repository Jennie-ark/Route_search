from django.db import models

from cities.models import City
from trains.models import Train


class Route(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            verbose_name='Название маршрута')

    travel_times = models.PositiveSmallIntegerField(
        verbose_name='Общее время в пути')

    from_city = models.ForeignKey(City, on_delete=models.CASCADE,
                                  related_name='route_from_city_set',
                                  verbose_name='Из какого города')

    to_city = models.ForeignKey(City, on_delete=models.CASCADE,
                                related_name='route_to_city_set',
                                verbose_name='В какой города')

    trains = models.ManyToManyField(Train, verbose_name='Список поездов')

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.across_cities = None

    def __str__(self):
        return f'Маршрут {self.name} из города {self.from_city}'

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ['travel_times']
