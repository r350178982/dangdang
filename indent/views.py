import time
import uuid

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
#渲染订单页面
from books.models import TBook
from cart.cart import Cart
from indent.models import TAddress, TOrder, TOrderitem
from user.models import TUser


def indent_page(request):

    #事件触发--点击购物车的结算按钮
    #1,首先判断用户是否已经登陆,获取登陆过后存储在session中的值
    username = request.session.get("username")

    #2,对username进行条件判断
    if username:
        #1获取购物车
        myCart = request.session.get("cart")
        sumPrice = myCart.sumPrice()
        savePrice = myCart.saveprice()
        itemList = myCart.bookItemList

        itemLength = len(itemList)

        #2获取地址
        #2.1获取用户信息
        user = TUser.objects.get(user_email=username)
        #2.2获取该用户下的地址信息
        addrs = TAddress.objects.filter(user=user)


        return render(request,"indent/indent.html",{"goodsInfo":itemList,
                                                    "sumPrice":sumPrice,
                                                    "addrInfo":addrs})
    else:
        #如果用户名不存在,则进入登陆页面,并且给一个标记

        request.session["flag"] = 1

        return redirect("User:user_login_page")

def indent_page_ajax(request):

    #1, 收集参数
    name = request.GET.get("name")
    user = request.session.get("username")

    #2,查询该姓名下的地址
    addr = TAddress.objects.get(name=name,user=TUser.objects.get(user_email=user))

    #3,返回Json
    return JsonResponse({"name":addr.name,
                         "addr":addr.detail_address,
                         "zipcode":addr.zipcode,
                         "cellphone":addr.cellphone,
                         "telphone":addr.telphone})

def indent_logic(request):
    #1,获取form表单的信息
    name = request.GET.get("ship_man")
    addr = request.GET.get("detail_addr")
    zipcode = request.GET.get("zipcode")
    cellphone = request.GET.get("cellphone")
    telphone = request.GET.get("telphone")

    #为了获得订单把name存入session
    request.session["addr_name"]=name

    #2,用户的登陆名,
    username = request.session.get("username")
    #3,查找该用户名的id
    user = TUser.objects.get(user_email=username)
    #2,判断在该登陆的用户名下姓名是否有重复的
    query_result = TAddress.objects.filter(name=name,user=user)
    print(query_result)

    #3,如果没有重复,则添加到数据库
    if not query_result:
        with transaction.atomic():

            TAddress(name=name,
                     detail_address=addr,
                     zipcode=zipcode,
                     cellphone=cellphone,
                     telphone=telphone,
                     user=TUser.objects.get(user_email=username)).save()

    return HttpResponse(1)

def indentOK_page(request):

    #1,获取购物车的信息
    myCart = request.session.get("cart")
    #2,获取订单的地址信息--通过保存的地址名称获取
    addr_name = request.session.get("addr_name")
    user = request.session.get("username")
    print(addr_name)
    #2.1通过该名称,获取订单对象
    addr = TAddress.objects.get(name=addr_name,user=TUser.objects.get(user_email=user))
    #3,获取订单中商品种类的数量
    num = len(myCart.bookItemList)
    #4,获取订单的总价
    price = myCart.sumPrice()
    #5,获取订单的生成日期
    creat_date = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    #6,获取用户信息
    username = request.session.get("username")
    user = TUser.objects.get(user_email=username)
    #7,用uuid当作订单的id
    order_id = str(uuid.uuid4()).replace("-",'')

    #获取订单项的相关信息
    #1, 获取购物车中的商品列表
    book_list = myCart.bookItemList

    with transaction.atomic():
        #保存订单
        myOrder = TOrder(id=order_id,
                num=num,
               create_date=creat_date,
               price=price,
               order_addrid=addr,
               order_uid=user,
               status=0)
        myOrder.save()

        # 保存订单项
        for i in book_list:

            TOrderitem(shop_num=i.amount,
                       total_price=i.amount*i.book.book_dprice,
                       shop_bookid=i.book,
                       shop_ordid=myOrder).save()


        # 订单生成之后需要减小商品的库存

        for i in book_list:

            book=TBook.objects.get(book_name=i.book.book_name)
            book.stock = book.stock-i.amount
            book.sales =book.sales+i.amount
            book.save()



    #删除购物车
    myCart.bookItemList=[]


    #查询订单信息
    orderInfo = TOrder.objects.get(status=0)

    #将订单的状态修改为0
    orderInfo.status = 1
    orderInfo.save()


    myCart = Cart()
    myCart_backup = Cart()
    request.session["cart"] = myCart
    request.session["cart_backup"] = myCart_backup



    return render(request,"indent/indent ok.html",{"orderInfo":orderInfo})





