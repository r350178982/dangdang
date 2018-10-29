from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from books.models import TCatagory, TBook


def book_list_page(request):

    main_catagory = TCatagory.objects.filter(category_pid__isnull=True)

    sub_catagory = TCatagory.objects.filter(category_pid__isnull=False)

    #1, 从页面获取图书分类的id
    cat_id = request.session.get("id")

    catInfo = TCatagory.objects.get(id = cat_id)
    #2, 若是一级分类的话, 其没有父id, 查询该id信息下的父id
    cat_pid = catInfo.category_pid

    #3, 查询返回图书列表页面
    if cat_pid is None: #当没有父id的时候说明此时点击的是图书的一级分类

        #获取该以及分类下的所有二级分类
        sub_cat = TCatagory.objects.filter(category_pid=cat_id)
        #把该以及分类下的二级分类的名称打包成一个列表
        l = []

        for i in sub_cat:

            l.append(i.category_name)
        #将该列表封装成一个元组
        t_cat = tuple(l)

        #查询属于该元组下的图书信息
        bookInfo = TBook.objects.filter(book_category__category_name__in=t_cat,book_status=1)
        maincatInfo = TCatagory.objects.get(id = cat_id)
        subcatInfo = None

    else:#当点击的内容有父id时,说明点击的是二级分类

        bookInfo = TBook.objects.filter(book_category=cat_id,book_status=1)
        sub_pid = TCatagory.objects.get(id = cat_id).category_pid

        maincatInfo = TCatagory.objects.get(id = sub_pid)

        subcatInfo = TCatagory.objects.get(id = cat_id)




    #排序
    sort_flag = request.GET.get("sort")

    if not sort_flag:
        bookInfo=bookInfo

    elif sort_flag == "0": #按照销量排序

        bookInfo = list(bookInfo)
        bookInfo.sort(key = lambda x:x.sales,reverse=True)

    elif sort_flag == "1": #按照价格排序
        bookInfo = list(bookInfo)
        bookInfo.sort(key=lambda x: x.book_dprice,reverse=True)
    elif sort_flag == "2":
        bookInfo = list(bookInfo)
        bookInfo.sort(key=lambda x: x.publish_time,reverse=True)


    # 获取书籍数量
    book_num = len(bookInfo)

    #分页功能
    pa = Paginator(object_list=bookInfo,per_page=5)
    page_num = request.GET.get("page_num")

    if page_num:
        page = pa.page(page_num)
    else:
        page = pa.page(1)

    response =  render(request,"books/booklist.html",{"page":page,
                                                 "maincatInfo":maincatInfo,
                                                 "subcatInfo":subcatInfo,
                                                 "main_category":main_catagory,
                                                 "sub_catagory":sub_catagory,
                                                      "book_num":book_num})


    return response



def book_detail_page(request):

    #1,获取参数
    book_id = request.GET.get("id")

    #2, 查找图书
    bookInfo = TBook.objects.get(pk=book_id)

    #3, 查找图书的分类
    cat_id = bookInfo.book_category.id

    sub_catagory = TCatagory.objects.get(pk = cat_id)
    main_id = sub_catagory.category_pid

    main_catagory = TCatagory.objects.get(pk = main_id)
    #3,渲染页面
    main_catagory_total = TCatagory.objects.filter(category_pid__isnull=True)
    return render(request,"books/Book details.html",{"bookInfo":bookInfo,
                                                     "main_catagory":main_catagory,
                                                     "sub_catagory":sub_catagory,
                                                     "main_catagory_total":main_catagory_total})