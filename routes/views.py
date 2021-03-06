from django.contrib import messages
from django.shortcuts import render, redirect

from trains.models import Train
from .forms import *

__all__ = (
    'home', 'find_routes', 'add_route', 'save_route'
)

from .utils import get_routes


def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def find_routes(request):
    if request.method == "POST":
        form = RouteForm(request.POST or None)
        context = {'form': form}
        if form.is_valid():
            print(form.cleaned_data)
            try:
                context = get_routes(request, form)
            except ValueError as e:
                messages.error(request, e)
                return render(request, 'routes/home.html', {'form': form})
        return render(request, 'routes/home.html', context)
    else:
        messages.error(request, 'Создайте маршрут')
        form = RouteForm()
        return render(request, 'routes/home.html', {'form': form})


def add_route(request):
    if request.method == 'POST':
        data = request.POST
        context = {}
        if data:
            _total_time = int(data['travel_times'])
            from_city_id = int(data['from_city'])
            to_city_id = int(data['to_city'])
            trains = data['trains'].split(',')
            trains_lst = [int(t) for t in trains if t.isdigit()]
            qs = Train.objects.filter(id__in=trains_lst).select_related(
                'from_city', 'to_city')
            cities = City.objects.filter(
                id__in=[from_city_id, to_city_id]).in_bulk()
            form = RouteModelForm(
                initial={
                    'from_city': cities[from_city_id],
                    'to_city': cities[to_city_id],
                    'travel_times': _total_time,
                    'trains': qs
                }
            )
            context['form'] = form
            return render(request, 'routes/create.html', context)
    else:
        # защита от обращения по адресу без данных
        messages.error(
            request, 'Невозможно сохранить несуществующий маршрут')
        return redirect('/')


def save_route(request):
    if request.method == "POST":
        form = RouteModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Маршрут успешно сохранен")
            return redirect('/')
        return render(request, 'routes/create.html', {'form': form})
    else:
        messages.error(request, "Невозможно сохранить несуществующий маршрут")
        return redirect('/')
