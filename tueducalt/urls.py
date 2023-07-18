"""tueducalt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home),
    path('accounts/', include('django.contrib.auth.urls'), name='login'),
    # path('campus/', TemplateView.as_view(template_name = 'campus.html')),
    path('campus/', views.campus, name="campus"),
    path('signup_2/', views.signup, name="signup_2"),
    path('api/', include('marketcourses.urls')),
    path('login/', views.login_campus, name="login"),
    path('logout/', views.logout_campus, name="logout"),
    path('register/', views.register, name="register"),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "registration/password_reset.html"), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"), name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_change_form.html"), name="password_reset_confirm"),
    
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name="password_reset_complete"),

] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
