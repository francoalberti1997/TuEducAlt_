from django.urls import path, include
from . import views

urlpatterns = [
    path('cursos/', views.get_product),
    path('files/', views.Archivos_pagina_LIST.as_view()),
    path('category_list/<int:id>/', views.GenericAPIView.as_view()),
    path('Category_detail/<int:pk>/', views.Category_detail.as_view()),
    path('category_list/', views.GenericAPIView.as_view()),
    path('estudiantes/<int:pk>', views.Estudiantes_API.as_view()),
    path('estudiantes/', views.Estudiantes_API.as_view()),
]