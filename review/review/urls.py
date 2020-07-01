
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from main.views import *

router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'review', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]