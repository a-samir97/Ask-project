"""Es2lany URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny
schema_view = get_schema_view(title="Es2alny API")

urlpatterns = [

    path('admin/', admin.site.urls),

    path('api/v1/accounts/',include('accounts.urls',namespace='accounts')),
    path('api/v1/questions/',include('ask.urls')),
    
    path('docs/',include_docs_urls(title='Es2alny API',public=True, permission_classes=(AllowAny,))),
    path('schema/', schema_view),
]
