from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('results.html', views.results, name='results'),
]