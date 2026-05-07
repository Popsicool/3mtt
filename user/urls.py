from django.urls import path
from user.views import *

urlpatterns = [
    path('', homepage, name="home"),
    path('about', aboutpage, name="about"),
    # path('contact', contactpagefunction, name="contact"),
    path('contact', ContactView.as_view(), name="contact"),
]