from rest_framework import serializers

from .models import Category, Product, Archivos_pagina, Estudiantes

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'name',
            'slug',
            'description',
            'price',
            'image',
            'thumbnail',
        )


class PageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archivos_pagina
        fields = (
            'name',
            'img',
        )


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'image',
        )

class EstudiantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiantes
        fields = "__all__"