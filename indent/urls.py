from django.contrib import admin
from django.urls import path, include

from indent import views

urlpatterns = [
    path("indent/",include([
        path("page/",views.indent_page,name="indent_page"),
        path("logic/",views.indent_logic,name="indent_logic"),
        path("ok/",views.indentOK_page,name="indent_ok_page"),
        path("ajax/",views.indent_page_ajax,name="indent_page_ajax"),

    ])),
]