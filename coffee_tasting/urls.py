"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from tasting_notes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_example/', views.add_example, name='add_example'),
    path('get_examples/', views.get_examples, name='get_examples'),
    path('add_user/', views.add_user, name='add_user'),
    path('get_users/', views.get_users, name='get_users'),
    path('add_coffee/', views.add_coffee, name='add_coffee'),
    path('get_coffees/', views.get_coffees, name='get_coffees'),
    path('edit_note/',views.edit_note, name = 'edit_note'),
    path('remove_note/',views.remove_note, name = 'remove_note'),
    path('login/', views.login_or_register, name='login_or_register'),
    path('get_user/<int:user_id>/', views.get_user_by_id, name='get_user_by_id'),
    path('add_review/', views.add_review, name='add_review'),
    path('add_user_review/', views.add_user_review, name='add_user_review'),
]

