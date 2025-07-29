"""
URL configuration for liblend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from library.views import *
from lending.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    # Library app views
    path('add_patron/', add_patron, name="add_patron"),
    path('add_book/', add_book, name="add_book"),

    # Lending app views
    path('make_loan/', make_loan, name="make_loan"),
    path('close_loan/', close_loan, name="close_loan"),
    path('join_waitlist/', join_waitlist),
]
