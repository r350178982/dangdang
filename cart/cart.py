"""
购物车功能:
    在此模块中定义与购物车相关的类,方便在view中处理请求中进行调用
"""

#定义购物车里面商品的类
from books.models import TBook


class CartItem:
    def __init__(self,book,amount):
        # 初始化书籍, 数据库中TBook类的对象
        self.book = book
        # 初始化书籍数量
        self.amount = amount






#定义购物车类, 可以对购物车商品进行增删该查
class Cart:
    def __init__(self):
        #1, 初始化购物车中的项目,用列表进行保存
        self.bookItemList = []
        #2, 初始化购物车中的价格总数
        self.totalPrice = 0
        #3, 初始节省的价格
        self.savePrice = 0

    #定义购物车的添加功能
    def addItem(self,bookid):
        #遍历商品列表看看里面有没有已经添加的书籍
        flag = 0
        for i in self.bookItemList:
            if i.book.id == bookid:
                i.amount+=1
                flag = 1

        if flag == 1:
            return
        else:
            book = TBook.objects.get(pk = bookid)
            self.bookItemList.append(CartItem(book,1))

    #定义购物车的删除功能
    def delItem(self,bookid):
        #查询图书,当项目的book对象的id等于传进来的bookid时执行remove
        #移除列表
        for i in self.bookItemList:
            if i.book.id == bookid:
                self.bookItemList.remove(i)

    def sumPrice(self):

        sum_price = 0

        for i in self.bookItemList:
            sum_price+=i.book.book_dprice*i.amount

        return sum_price

    def saveprice(self):

        savep = 0
        for i in self.bookItemList:
            savep+=(i.book.book_price-i.book.book_dprice)*i.amount

        return savep


    def addByAmount(self,amount,bookid):

        for i in range(amount):

            self.addItem(bookid)


    def updateItem(self,amount,bookid):

        for i in self.bookItemList:

            if i.book.id == bookid:
                i.amount = amount





