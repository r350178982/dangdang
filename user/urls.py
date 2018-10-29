from django.contrib import admin
from django.urls import path, include

from user import views

urlpatterns = [
    path('register/', include([
        path("page/",views.user_register_page,name="user_register_page"),
        path("captcha/",views.captcha,name="captcha"),
        path("cap_check/",views.check_captcha,name="cap_check"),
        path("logic/",views.user_register_logic,name="user_register_logic"),
        path("ok/",views.register_ok_page,name="register_ok_page"),
        path("ok_logic/",views.register_ok_logic,name="register_ok_logic"),
    ])),

    path('login/',include([
        path("page/",views.user_login_page,name="user_login_page"),
        path("logic/",views.user_login_logic,name="user_login_logic"),
        path("out/",views.user_logout_logic,name="user_logout_logic"),
    ]))

]