from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.

#渲染项目主页的页面
from books.models import TBook, TCatagory



def main_page(request):

    #查询数据库--类别库
    #1, 查询一级分类
    main_catagory = TCatagory.objects.filter(category_pid__isnull=True)



    #2, 查询二级分类
    sub_catagory = TCatagory.objects.filter(category_pid__isnull=False)


    #3, 查询编辑推荐图书, 从高到底选出前八个
    recommend_book = TBook.objects.all().order_by("-editor_recommendation")[0:10]

    #4, 查询新书, 按照上架时间进行排序
    shelf_book_new = TBook.objects.all().order_by("-shelves_date")[0:8]

    #5, 新书热卖榜
    new_sale_book = TBook.objects.all().order_by("-sales","-shelves_date")
    return render(request,"main/index.html",{"main_category":main_catagory,
                                             "sub_catagory":sub_catagory,
                                             "recommend_book":recommend_book,
                                             "shelf_book_new":shelf_book_new,
                                             "new_sale_book":new_sale_book})


#点击分类按钮,返回图书的列表
def main_logic(request):


    #1, 从页面获取图书分类的id
    cat_id = request.GET.get("id")

    request.session["id"] = cat_id

    return redirect("Books:book_list_page")









