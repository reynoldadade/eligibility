"""testPy URL Configuration

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
from django.urls import path, include
from django.conf.urls import url
from .views import login_view, logout_view, landing_page_view, http403_view, http404_view,http500_view


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', login_view),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^landing_page/', landing_page_view, name='landing_page'),
    url(r'^eligibility/', include('eligibility.urls'))
]

handler403 = http403_view
handler404 = http404_view
handler500 = http500_view

admin.site.site_header = 'Eligibility App Admin'
admin.site.site_title = 'Eligibility App Admin'

