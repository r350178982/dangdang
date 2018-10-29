import hashlib
import os
import random
import re
import string

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from user.captcha.image import ImageCaptcha
from user.models import TUser

'''
设计注册模块的视图逻辑(包括):
    1, 渲染注册页面
    2, 接收template的请求参数
    3, 根据表单中的要求, 判断请求参数的格式是否合法
    4, 使用正则表达式去限定输入参数的格式
    5, 用return HttpResponse来异步返回参数的逻辑处理结果
    6, 根据异步返回的结果, 在模板中设置blur事件, 给用户提示信息(Ajax)
    7, 验证码的生成与回想
'''

# 1, 渲染注册页面的view
def user_register_page(request):
    """
    使用render来渲染指定的用户注册页面
    :param request:
    :return:
    """
    return render(request,'user/register.html')

# 2, 在页面中添加验证码
def captcha(request):

    #1, 生成验证码的格式转换器
    image = ImageCaptcha(fonts=[os.path.abspath("captcha/fonts/AdobeFanHeitiStd-Bold.otf")])

    #2, 生成随机的四位字符
    code = ''.join(random.sample(string.ascii_lowercase+string.ascii_uppercase+string.digits,4))

    #3, 将生成的验证码存入session
    request.session['captcha_code'] = code

    #4, 将号码用图片和格式进行转化
    data = image.generate(code)

    #5, 将验证码信息写出给模板
    return HttpResponse(data,"image/png")

#定义正则表达式
def mathch_username(username):

    #1, 定义邮箱的正则规则
    rule_email = '\w{3,}@\w{2,}\.com|\w{3,}@\w{2,}\.cn|\w{3,}@\w{2,}\.org'
    #2, 定义手机的正则规则
    rule_phone = '^[1][358][0-9]{9}$'

    #3, 进行匹配
    match_email = re.findall(rule_email,username)
    match_phone = re.findall(rule_phone,username)

    #4, 进行判断
    if match_email or match_phone:
        return True
    else:
        return False

# 3, 定义注册逻辑的view
def user_register_logic(request):

    #获取异步传来的用户名
    username = request.GET.get("username")
    #获取异步传来的密码


    #获取异步传来的验证码
    #逻辑处理
    #1,对用户名进行处理
    #1.1 判断用户名的格式是否符合要求
    if mathch_username(username):
        # 判断用户名是否和数据库重复
        if TUser.objects.filter(user_email=username):

            return HttpResponse("user_repeat")
        else:
            request.session["username"] = username
            return HttpResponse("user_ok")

    else:

        return HttpResponse("user_wrong")

    #2,对密码进行处理---略已经在前端用js进行编写

#定义验证验证码的view
def check_captcha(request):
    #3,对验证码进行处理
    #3.1获取真实验证码


    #进行比较
    cap_code = request.GET.get("cap_code")
    real_code = request.session.get("captcha_code")

    if cap_code.lower() == real_code.lower():

        return HttpResponse("cap_code_ok")

    else:

        return HttpResponse("cap_code_wrong")

#定义注册成功页面
def register_ok_page(request):

    return render(request,"user/register ok.html")

#加密算法
def salt_generation():
    random_code = "".join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits, 6))
    return random_code

def pwd_encryption(password,salt):

    #1,定义随机字符串

    #2,将密码和随机字符串进行拼接
    code = salt+password
    #3,创建对象
    h=hashlib.md5()
    #4,将密码加入进行处理
    h.update(code.encode())

    #5,加密结果收餐
    result = h.hexdigest()

    #6,
    return result

#定义注册成功逻辑
def register_ok_logic(request):

    #定义注册成功的逻辑, 将用户名密码储存与数据库
    #1, 从session中获取临时保存的用户名和密码
    username = request.session.get("username")
    password = request.GET.get("password")
    #将密码进行加密放入数据库
    random_code = salt_generation()
    en_password = pwd_encryption(password,random_code)
    #2, 保存值数据库
    TUser(user_email=username,user_password=en_password,user_salt=random_code).save()

    #3, 跳转成功页面
    return redirect("User:register_ok_page")



#定义登陆逻辑
def user_login_page(request):

    return render(request,"user/login.html")


def user_login_logic(request):

    #1,接收参数
    username = request.GET.get("username")
    password = request.GET.get("password")
    print(username)
    print(password)
    #2,查询数据库进行比较
    userInfo = TUser.objects.filter(user_email=username)
    #3,从数据库中获取位置标记
    flag = request.session.get("flag")
    if userInfo:

        #查询密码
        user_pwd = userInfo[0].user_password
        user_salt = userInfo[0].user_salt
        #将传进来的密码和salt拼接进行转换
        user_pwd1 = pwd_encryption(password,user_salt)

        if user_pwd == user_pwd1:

            request.session['username'] = username
            if flag:#寿命是从购物车结算页面进行跳转
                request.session["flag"] = 0
                return HttpResponse(2)
            else:
                request.session["flag"] = 0
                return HttpResponse(1)

        else:

            return HttpResponse(0)

    else:

        return HttpResponse(0)

#定义登出逻辑
def user_logout_logic(request):

    del request.session['username']

    return redirect("DangDang:main_page")


