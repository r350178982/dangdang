from django.contrib import admin
from django.urls import path, include

from main import views

urlpatterns = [
    path('main/',include([
        path('page/',views.main_page,name="main_page"),
        path('logic/',views.main_logic,name="main_logic")

    ])),


]
