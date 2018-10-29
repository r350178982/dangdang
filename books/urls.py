from django.contrib import admin
from django.urls import path, include

from books import views

urlpatterns = [
    path('book/', include([
        path('list/', views.book_list_page, name="book_list_page"),
        path('detail/', views.book_detail_page, name="book_detail_page")
    ]))
]