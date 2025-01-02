from django.urls import path
from . import views

urlpatterns = [
    path("acer/", views.AcerLaptopListApiView.as_view(), name='acer-laptops'),
    path("acer/<int:id>/", views.AcerLaptopListApiView.as_view(), name='acer-laptops-detail'),
]