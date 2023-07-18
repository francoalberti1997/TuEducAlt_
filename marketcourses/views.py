from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Archivos_pagina, Category, Estudiantes
from .serializers import ProductSerializer, PageFileSerializer, EstudiantesSerializer, CategoriaSerializer
from rest_framework import status
from rest_framework import generics, mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from tueducalt.decorators import unauthenticated_user, allowed_users


class Archivos_pagina_LIST(APIView):
    def get(self, request, format = None):
        files = Archivos_pagina.objects.all()
        serializer = PageFileSerializer(files, many=True)
        return Response(serializer.data)
    
# class LatestProductsList(APIView):
#     def get(self, request, format = None):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)

@api_view(['GET', 'POST'])
# @allowed_users(allowed_roles = ["admin"])

def get_product(request, *args, **kwargs):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# class Category_list(APIView):
#     def get(self, request, format = None):
#         category = Category.objects.all()
#         serializer = CategoriaSerializer(category, many=True)
#         return Response(serializer.data)    

#     def post(self, request):
#         serializer = CategoriaSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, 
                     mixins.UpdateModelMixin , mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    
    serializer_class = CategoriaSerializer
    queryset = Category.objects.all()
    lookup_field = 'id'
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.update(request, *args, **kwargs)
        else:
            # Manejar el caso en el que no se proporciona un ID
            return self.http_method_not_allowed(request, *args, **kwargs)
        
    def delete(self, request, id):
        return self.destroy(request, id)
        
class Category_detail(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(id=pk)
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = CategoriaSerializer(article)
        return Response(serializer.data)
    
    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = CategoriaSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_200_OK)

      
class Estudiantes_API(APIView):
    def get_object(self, pk):
        try:
            return Estudiantes.objects.get(id=pk)
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk=None):
        if pk:
            article = self.get_object(pk)
            serializer = EstudiantesSerializer(article)
            print("SALIDA")
            print(article.imagen)
            print("SALIDA")
            return Response(serializer.data)
        else:
            article = Estudiantes.objects.all()
            serializer = EstudiantesSerializer(article, many=True)
            return Response(serializer.data)
    
    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = EstudiantesSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        serializer = EstudiantesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)