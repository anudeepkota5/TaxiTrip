"""TaxiTrip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
import taxiview.views
from django.views.generic.base import TemplateView
admin.autodiscover()

urlpatterns = [
    url('admin/', admin.site.url),
    url(r'^index/', TemplateView.as_view(template_name = 'index.html'), name = 'index'),
    url(r'^predictions/', taxiview.views.predictions, name = "predictions"),
]
