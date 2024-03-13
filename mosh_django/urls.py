"""
URL configuration for mosh_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from rest_framework.documentation import include_docs_urls

admin.site.site_header = "Mesutfd Web"
admin.site.index_title = "Goddess"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('changes.urls')),
    path('api/docs/', include_docs_urls(title='Mesutfd Docs')),
    path('playground/', include('playground.urls')),
    path('store/', include('store.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]
