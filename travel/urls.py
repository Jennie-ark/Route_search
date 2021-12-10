from django.contrib import admin
from django.urls import path, include

import accounts
from routes.views import home, find_routes, add_route, save_route

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('find_routes/', find_routes, name='find_routes'),
    path('cities/', include(('cities.urls', 'cities'))),
    path('trains/', include(('trains.urls', 'trains'))),
    path('add_route/', add_route, name='add_route'),
    path('save_route/', save_route, name='save_route'),
    path('accounts/', include(('accounts.urls', 'accounts'))),
]
