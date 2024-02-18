from django.contrib import admin
from django.urls import path, include
from Truck.views import TruckModelCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('location/', TruckModelCreateView.as_view(), name="truck"),
    path('explorer/', include('explorer.urls')),
]
