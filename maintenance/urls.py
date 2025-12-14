from django.urls import path
from maintenance import views

urlpatterns = [
    path('', views.list_urls),
    path('preventives/get/', views.maintenanceWithFiltering),
]