from django.shortcuts import render, redirect, resolve_url
from django.contrib import messages
from django.views import View
from user.models import ContactMessage
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def homepage(request):
    print(request.method)
    return render(request, 'home.html')

@login_required
def aboutpage(request):
    return render(request, 'about.html')

def contactpagefunction(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        if not name or not email or not message:
            messages.error(request, "All fields are required")
            return render(request, 'contact.html')
        if len(name) < 2:
            messages.warning(request, "Name is too short")
            return render(request, 'contact.html')
        
        #? do something with what they submitted
        messages.success(request, "Your message has been received, we will be in touch!")
        return redirect(homepage)
    elif request.method == "PUT":
        pass
    elif request.method == "PATCH":
        pass
    elif request.method == "DELETE":
        pass
    else:
        return render(request, 'contact.html')



class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')
    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        if not name or not email or not message:
            messages.error(request, "All fields are required")
            return render(request, 'contact.html')
        if len(name) < 2:
            messages.error(request, "Name is too short")
            return render(request, 'contact.html')
        if len(name) > 250:
            messages.error(request, "Name is too long")
            return render(request, 'contact.html')
        
        #? do something with what they submitted
        ContactMessage.objects.create(name = name, email=email, message=message)
        messages.success(request, "Your message has been received, we will be in touch!")
        return redirect(homepage)