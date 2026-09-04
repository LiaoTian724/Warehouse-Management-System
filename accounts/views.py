
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        real_name = request.POST["real_name"]
        password = request.POST["password"]


        # 登录名统一小写
        username = username.lower()

        # 检查p开头
        if not username.startswith("p"):
            return render(
                request,
                "accounts/register.html",
                {"error":"账号必须以P开头"}
            )

        # 检查用户名是否存在
        if User.objects.filter(username=username).exists():
            return render(
                request,
                "accounts/register.html",
                {"error":"该账号已经存在，请更换账号"}
            )
        
        # 姓名格式化
        real_name = (real_name[0].upper()  +  real_name[1:].lower())
        if not real_name:
            return render(
                request,
                "accounts/register.html",
                {"error":"请输入姓名拼音"}
            )
        user = User.objects.create_user(
            username=username,
            password=password
        )


        UserProfile.objects.create(
            user=user,
            real_name=real_name,
            role="USER",   # 普通用户
            status="PENDING"  # 等待管理员审核
        )


        return redirect("login")


    return render(
        request,
        "accounts/register.html"
    )



def login_view(request):
    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            return render(
                request,
                "accounts/login.html",
                {"error":"用户名或密码错误"}
            )


            
        # 超级管理员直接登录
        if user.is_superuser:
            login(request, user)
            return redirect("/")

        profile = user.userprofile

        if profile.status != "APPROVED":
                return render( request, "accounts/login.html", 
                            {"error": "账号正在审核，请等待管理员批准"})

        login(request,user)
        return redirect("/")                    

    return render(
        request,
        "accounts/login.html"
    )





@login_required
def approve_users(request):
    # 判断管理员
    profile = request.user.userprofile

    if profile.role != "ADMIN":
        return HttpResponse("没有权限")

    users = UserProfile.objects.filter(status="PENDING")

    return render(
        request,
        "accounts/approve_users.html",
        {"users": users}
    )



def logout_view(request):
    logout(request)
    return redirect("login")