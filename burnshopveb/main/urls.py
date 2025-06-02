from django.urls import path
from .views import home, search_results

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_results, name='search_results'),
]