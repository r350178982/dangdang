from django.contrib import admin
from django.urls import path, include

from myadmin import views

urlpatterns = [
    path("myadmin/",include([
        path("index/",views.admin_page,name="myadmin_page"),
        path("add/",include([
            path("page/",views.add_page,name="add_page"),
            path("ajax/",views.add_ajax,name="add_ajax"),
            path("logic/",views.add_logic,name="add_logic"),
        ])),





        path("dzlist/",views.dzlist_page,name="dzlist_page"),

        path("list/",include([
            path("page/",views.list_page,name="list_page"),
            path("logic/",views.list_logic,name="list_logic"),
            path("package/",views.package_logic,name="package_logic"),
            path("perpage/",views.list_per_page,name="list_per_page"),
        ])),

        path("splb/",views.splb_page,name="splb_page"),
        path("test/",views.test_page,name="test_page"),
        path("zjlb/",include([
            path("page/",views.zjlb_page,name="zjlb_page"),
            path("logic/",views.zjlb_logic,name="zjlb_logic"),


        ])),
        path("zjzlb/",include([
            path("page/",views.zjzlb_page,name="zjzlb_page"),
            path("logic",views.zjzlb_logic,name="zjzlb_logic"),
        ])),
    ])),


]