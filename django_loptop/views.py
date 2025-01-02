from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from .models import Loptop
from .serializers import LoptopSerializer


class AcerLaptopListApiView(APIView):  
    serializer_class = LoptopSerializer  

    def get_permissions(self):  
        if self.request.method in ['DELETE', 'POST', 'PUT']:  
            return [IsAdminUser()]  
        return [AllowAny()]  

    def get_queryset(self):  
        return Loptop.objects.filter(brand='ACER')  

    def get(self, request, id=None):  
        if id:  
            laptop = get_object_or_404(Loptop, id=id)  
            serializer = LoptopSerializer(laptop)  
            return Response(serializer.data, status=status.HTTP_200_OK)  

        laptops = self.get_queryset()  
        paginator = PageNumberPagination()
        results_page = paginator.paginate_queryset(laptops, request)
        
        return paginator.get_paginated_response(LoptopSerializer(results_page, many=True).data)  

    def post(self, request):  
        serializer = LoptopSerializer(data=request.data)  
        if serializer.is_valid():  
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

    def put(self, request, id):  
        laptop = get_object_or_404(Loptop, id=id)  
        serializer = LoptopSerializer(laptop, data=request.data)  
        if serializer.is_valid():  
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_200_OK)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    def delete(self, request, id):  
        laptop = get_object_or_404(Loptop, id=id)  
        laptop.delete()  
        return Response(status=status.HTTP_204_NO_CONTENT)