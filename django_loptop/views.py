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
    brand = filters.CharFilter(field_name='brand', lookup_expr='icontains', help_text='Filter by brand name (e.g. Acer, Dell)')
    model = filters.CharFilter(field_name='model', lookup_expr='icontains', help_text='Filter by model name (e.g. Aspire 5, Inspiron 15)')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains', help_text='Filter by Farsi title (e.g. مانند گیمینگ)')
    specs = filters.CharFilter(field_name='specs', lookup_expr='icontains', help_text='Filter by specifications (e.g. 16GB RAM, 512GB SSD)')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte', help_text='Filter by lower than or equal to price (e.g. 1000000)')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte', help_text='Filter by upper than or equal to price (e.g. 2000000)')
    
    class Meta:
        model = Laptop
        fields = ['brand', 'model', 'title', 'specs', 'min_price', 'max_price']


class LaptopListApiView(ListAPIView):  
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
        id = kwargs.get('id')
        if id:
            laptop = get_object_or_404(Laptop, id=id)
            serializer = LoptopSerializer(laptop)
            return Response(serializer.data)
        response = super().get(request, *args, **kwargs)  
        return Response({  
            'help_text': {  
                'brand': 'Filter by brand name (e.g. Acer, Dell)',  
                'model': 'Filter by model name or number',  
                'title': 'Filter by laptop name',  
                'specs': 'Filter by specifications (e.g., RAM, HDD)',  
                'min_price': 'Minimum price to filter laptops',  
                'max_price': 'Maximum price to filter laptops',  
            },  
            'results': response.data  
        })

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


