from django.urls import path
from . import views

urlpatterns = [
    path("", views.LaptopListApiView.as_view(), name='laptops'),
    path("<int:id>/", views.LaptopListApiView.as_view(), name='laptop-detail'),
]