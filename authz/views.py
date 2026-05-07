from django.shortcuts import render, redirect, resolve_url
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


# Create your views here.


class SignUpView(View):
    def get(self, request):
        return render(request, 'signup.html')
    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        password = request.POST.get("password")
        if not username or not email or not firstname or not lastname or not password:
            messages.error(request, "All fields are required")
            return render(request, 'signup.html')
        if len(password) < 8:
            messages.error(request, "Password is too short")
            return render(request, 'signup.html')
        if len(username) < 5:
            messages.error(request, "Username is too short")
            return render(request, 'signup.html')
        

        username = username.lower()
        email = email.lower()

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken")
            return render(request, 'signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken")
            return render(request, 'signup.html')
        user = User.objects.create(username=username,
                                   email=email,
                                   first_name = firstname,
                                   last_name = lastname
                                   )
        user.set_password(password)
        user.save()
        # Send welcome email
        messages.success(request, "Account created successfully!")
        return redirect (resolve_url('home'))



def loginview(request):
    if request.method == "POST":
        next_page = request.GET.get("next")

        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            messages.error(request, "All fields are required")
            return render(request, "login.html")
        username = username.lower()
        username_exist = User.objects.filter(username = username).first()
        if not username_exist:
            messages.error(request, "Invalid login credentials")
            return render(request, "login.html")
        user = authenticate(username=username, password=password)
        if not user:
            messages.error(request, "Invalid login credentials")
            return render(request, "login.html")
        login(request, user)
        messages.success(request, "Login successful!")
        return redirect( next_page or resolve_url('home'))

        
    return render(request, "login.html")

def logoutview(request):
    logout(request)
    return redirect(loginview)