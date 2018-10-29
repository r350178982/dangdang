from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from books.models import TBook
from cart.cart import Cart,CartItem
# Create your views here.
def cart_page(request):

    cartInfo = request.session.get("cart")
    delInfo = request.session.get("cart_backup")

    if not cartInfo:
        cartInfo=Cart()

    if delInfo:
        delList = delInfo.bookItemList
    else:
        delList = []
    sumPrice = cartInfo.sumPrice()
    savePrice = cartInfo.saveprice()
    itemList = cartInfo.bookItemList

    itemLength = len(itemList)


    return render(request,"cart/car.html",{"sumPrice":sumPrice,
                                           "savePrice":savePrice,
                                           "bookInfo":itemList,
                                           "delList":delList,
                                           "goodsAmount":itemLength})

def add_item_logic(request):

    #定义添加商品的逻辑
    #1,接收参数
    book_id = int(request.GET.get("id"))

    #,从session中获取购物车
    myCart = request.session.get("cart")

    #,判断购物车是否存在
    if myCart:

        #存在进行添加功能
        myCart.addItem(book_id)
        request.session["cart"] = myCart

        return HttpResponse(1)



    else: #若不存在

        myCart = Cart()
        myCart.addItem(book_id)
        request.session["cart"] = myCart

        return HttpResponse(1)


def del_item_logic(request):
    #收集参数
    book_id = int(request.GET.get("id"))
    print(book_id)
    #获取session中的购物车对象
    myCart = request.session.get("cart")

    #调用其删除功能
    myCart.delItem(book_id)

    #更新session
    request.session["cart"] = myCart

    #从session中获取购物车恢复对象
    myCart_backup = request.session.get("cart_backup")
    if myCart_backup: #若垃圾车存在

        myCart_backup.addItem(book_id)
        request.session["cart_backup"] = myCart_backup

    else: #若垃圾车不存在

        myCart_backup = Cart()
        myCart_backup.addItem(book_id)
        request.session["cart_backup"] = myCart_backup

    return redirect("Cart:cart_page")

def del_item_package(request):

    myCart = request.session.get("cart")
    myCart_backup = request.session.get("cart_backup")
    book_id_str = request.GET.get("id")

    book_id_str_list = book_id_str.split(",")
    book_id_str_list.pop()

    book_id_list = [int(i) for i in book_id_str_list]

    print(book_id_list)


    for book_id in book_id_list:


        myCart.delItem(book_id)
        myCart_backup.addItem(book_id)

    request.session["cart"] = myCart
    request.session["cart_backup"] = myCart_backup





    return redirect("Cart:cart_page")


def renew_item_logic(request):

    #定义购物车恢复功能, 点击恢复,从恢复区回到购物车
    #收集参数
    book_id = int(request.GET.get("id"))
    #获取垃圾车
    myCart_backup = request.session.get("cart_backup")
    #获取购物车
    myCart = request.session.get("cart")

    #进行恢复,垃圾车删除商品, 购物车添加商品
    myCart_backup.delItem(book_id)
    myCart.addItem(book_id)

    #恢复之后存入session
    request.session["cart"] = myCart
    request.session["cart_backup"] = myCart_backup

    return redirect("Cart:cart_page")

def del_forever_logic(request):
    #获取垃圾车对象
    cart_backup = request.session.get("cart_backup")
    #获取图书id
    book_id = int(request.GET.get("id"))
    #删除图书
    cart_backup.delItem(book_id)
    #更新session
    request.session["cart_backup"] = cart_backup

    #返回响应
    return redirect("Cart:cart_page")

def update_item_logic(request):

    book_amount = int(request.GET.get("amount"))
    book_id = int(request.GET.get("id"))

    #查询库存
    book_stock = TBook.objects.get(pk=book_id).stock

    #获取购物车
    myCart = request.session.get("cart")
    #更新购物车
    myCart.updateItem(book_amount,book_id)
    #存入session
    request.session["cart"] = myCart
    #店铺合计
    sumPrice = myCart.sumPrice()
    savePrice = myCart.saveprice()



    return JsonResponse({"sumPrice":sumPrice,
                         "savePrice":savePrice,
                         "stock":book_stock})

def update_amount_logic(request):
    book_amount = int(request.GET.get("amount"))
    book_id = int(request.GET.get("id"))

    # 获取购物车
    myCart = request.session.get("cart")
    # 更新购物车
    if myCart:
        myCart.addByAmount(book_amount, book_id)
    else:
        myCart=Cart()
        myCart.addByAmount(book_amount, book_id)
    # 存入session
    request.session["cart"] = myCart

    return HttpResponse(1)

