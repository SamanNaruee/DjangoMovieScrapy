from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from .models import Laptop
from .serializers import LoptopSerializer

class LaptopFilter(filters.FilterSet):
    brand = filters.CharFilter(field_name='brand', lookup_expr='icontains')
    model = filters.CharFilter(field_name='model', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    specs = filters.CharFilter(field_name='specs', lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    class Meta:
        model = Laptop
        fields = ['brand', 'model', 'name', 'specs', 'min_price', 'max_price']


class AcerLaptopListApiView(ListAPIView):  
    serializer_class = LoptopSerializer 
    pagination_class = PageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LaptopFilter

    def get_permissions(self):  
        if self.request.method in ['DELETE', 'POST', 'PUT']:  
            return [IsAdminUser()]  
        return [AllowAny()]  

    def get_queryset(self):  
        return Laptop.objects.all() 

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request):  
        serializer = LoptopSerializer(data=request.data)  
        if serializer.is_valid():  
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

    def put(self, request, id):  
        laptop = get_object_or_404(Laptop, id=id)  
        serializer = LoptopSerializer(laptop, data=request.data)  
        if serializer.is_valid():  
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_200_OK)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    def delete(self, request, id):  
        laptop = get_object_or_404(Laptop, id=id)  
        laptop.delete()  
        return Response(status=status.HTTP_204_NO_CONTENT)


