import time

from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from books.models import TBook, TCatagory
from indent.models import TAddress


def admin_page(request):


    return render(request,'myadmin/index.html')

#书籍商品增加页面
def add_page(request):

    #查询父类名称
    main_cat = TCatagory.objects.filter(category_pid__isnull=True)
    return render(request,"myadmin/main/add.html",{"catInfo":main_cat})

#定义商品类别选择的异步请求
def add_ajax(request):
    #获取异步传来的父类
    main_cat = request.GET.get("main_cat")
    main_cat_info = TCatagory.objects.get(category_name=main_cat)

    #查询该父类下所有的子类
    sub_cat = TCatagory.objects.filter(category_pid=main_cat_info.id)
    if sub_cat:
    #获取该子类的名称
        sub_cat_name = [i.category_name for i in sub_cat]


        return JsonResponse({"myname":sub_cat_name})

    else:

        return HttpResponse(0)


#书籍商品增加逻辑
def add_logic(request):

    # 1,接收form表单的参数
    book_name = request.POST.get("book_name")
    print(book_name)
    book_author = request.POST.get("book_author")
    book_publish = request.POST.get("book_publish")
    book_category = request.POST.get("book_category")

    #查询在该类型下对应的父类
    sub_cat = TCatagory.objects.get(category_name=book_category)
    main_cat = TCatagory.objects.get(pk=sub_cat.category_pid)

    publish_time = request.POST.get("publish_time")
    book_price = float(request.POST.get("book_price"))
    book_dprice = float(request.POST.get("book_dprice"))
    stock = request.POST.get("stock")
    shelves_date = time.strftime("%Y-%m-%d",time.localtime())
    cover_img = request.FILES.get("cover_img")

    # 存入数据库
    with transaction.atomic():
        TBook(book_name=book_name,
              book_author=book_author,
              book_publish=book_publish,
              book_category=sub_cat,
              publish_time=publish_time,
              book_price=book_price,
              book_dprice=book_dprice,
              book_status=1,
              stock=stock,
              sales=0,
              shelves_date=shelves_date,
              product_image_path=cover_img).save()

    return redirect("Myadmin:add_page")








#地址列表
def dzlist_page(request):

    #1, 从数据库中获取地址信息
    addrInfo = TAddress.objects.all()

    return render(request,"myadmin/main/dzlist.html",{"addrInfo":addrInfo})




#书籍商品列表
def list_page(request):
    # 1, 从数据库中获取书籍信息
    bookInfo = TBook.objects.all()
    #1,定义图书列表的排序规则,从页面获取参数
    sort_flag = request.GET.get("sort_flag")

    if not sort_flag:
        bookInfo= list(bookInfo)
        bookInfo.sort(key=lambda x:x.book_status,reverse=True)
        # return render(request, "myadmin/main/list.html", {"bookInfo": bookInfo})
    elif sort_flag == "1": #销量升序排列
        bookInfo = list(bookInfo)
        bookInfo.sort(key=lambda x:x.sales)
        # return render(request, "myadmin/main/list.html", {"bookInfo": bookInfo})
    elif sort_flag == "2":#销量降序排列
        bookInfo = list(bookInfo)
        bookInfo.sort(key=lambda x: x.sales,reverse=True)
        # return render(request, "myadmin/main/list.html", {"bookInfo": bookInfo})
    elif sort_flag == "3":#上架日期升序
        bookInfo = list(bookInfo)
        bookInfo.sort(key=lambda x: x.shelves_date)
        # return render(request, "myadmin/main/list.html", {"bookInfo": bookInfo})
    elif sort_flag == "4":#上架日期降序
        bookInfo = list(bookInfo)
        bookInfo.sort(key=lambda x: x.shelves_date,reverse=True)

    num_per_page = request.session.get("num_per_page")

    if not num_per_page:

        pa = Paginator(object_list=bookInfo, per_page=20)
    else:

        pa = Paginator(object_list=bookInfo, per_page=num_per_page)

    page_num = request.GET.get("num")

    if page_num:
        page = pa.page(page_num)
    else:
        page = pa.page(1)


    return render(request, "myadmin/main/list.html", {"page": page})

def list_per_page(request):

    #定义每页显示多少条的逻辑
    num_per_page = request.GET.get("num_per_page")

    request.session["num_per_page"] = num_per_page

    #
    return redirect("Myadmin:list_page")

def list_logic(request):

    #1,定义商品的下架逻辑
    #收集参数
    book_id = request.GET.get("id")

    #把书籍的上架状态修改
    bookInfo = TBook.objects.get(pk=book_id)
    if bookInfo.book_status==1:
        bookInfo.book_status=0
        bookInfo.save()
    else:
        bookInfo.book_status=1
        bookInfo.shelves_date=time.strftime("%Y-%m-%d",time.localtime())
        bookInfo.save()

    return redirect("Myadmin:list_page")


def package_logic(request):

    #定义图书批量下架的逻辑
    book_id_str = request.GET.get("id")

    book_id_str_list = book_id_str.split(",")
    book_id_str_list.pop()

    book_id_list = [int(i) for i in book_id_str_list]

    #批量进行下架
    for i in book_id_list:
        bookInfo = TBook.objects.get(pk=i)

        if bookInfo.book_status == 1:
            bookInfo.book_status = 0
            bookInfo.save()
        else:
            bookInfo.book_status = 1
            bookInfo.save()
    return redirect("Myadmin:list_page")

def splb_page(request):

    #1, 查找所有商品
    bookInfo = TBook.objects.all()

    #2,定义空列表
    cat_list = []

    #3,
    for i in bookInfo:

        cat_list.append({"cat_id":i.id,
                         "sub_cat":i.book_category.category_name,
                         "main_cat":TCatagory.objects.get(pk=i.book_category.category_pid).category_name})


    return render(request,"myadmin/main/splb.html",{"cat_list":cat_list})


def test_page(request):


    return render(request,"myadmin/main/test.html")


def zjlb_page(request):


    return render(request, "myadmin/main/zjlb.html")

def zjlb_logic(request):
    #定义增加类别逻辑
    #1,接收参数
    main_cat = request.GET.get("main_cat")

    if TCatagory.objects.filter(category_name=main_cat):
        return HttpResponse(0)
    else:
    #2,更新数据库
        TCatagory(category_name=main_cat,book_counts=0).save()
        return HttpResponse(1)






def zjzlb_page(request):

    #查询所有父类别
    main_cat = TCatagory.objects.filter(category_pid__isnull=True)
    return render(request,"myadmin/main/zjzlb.html",{"main_cat":main_cat})



def zjzlb_logic(request):

    #定义增加子类别的逻辑
    main_cat = request.GET.get("main_cat")

    sub_cat = request.GET.get("sub_cat")

    #查询该父类别下的所有子类别

    mainInfo = TCatagory.objects.get(category_name=main_cat)
    subInfo = TCatagory.objects.filter(category_pid=mainInfo.id,category_name=sub_cat)


    #条件判断
    if subInfo:

        return HttpResponse(0)

    else:

        TCatagory(category_pid=mainInfo.id,category_name=sub_cat,book_counts=0).save()
        return HttpResponse(1)