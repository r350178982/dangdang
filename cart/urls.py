

from django.urls import include, path

from cart import views

urlpatterns = [
    path('cart/', include([
        path('page/', views.cart_page, name="cart_page"),
        path('add/', views.add_item_logic, name="add_item_logic"),
        path('del/', views.del_item_logic, name="del_item_logic"),
        path('renew/', views.renew_item_logic, name="renew_item_logic"),
        path('update/', views.update_item_logic, name="update_item_logic"),
        path('amount/',views.update_amount_logic,name="update_amount_logic"),
        path('forever/', views.del_forever_logic, name="del_forever_logic"),
        path('delpack/', views.del_item_package, name="del_item_package"),

    ])),
]