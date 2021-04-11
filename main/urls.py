from django.contrib import admin
from django.urls import path, include
from .views import homepage,testing, company_view
from graph.views import Graph

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage, name='home'),
    path('company/<str:company>',company_view, name="companypage"),
    path('test/<int:year>',testing, name='testing'),
    path('', include('graph.urls')),
]
