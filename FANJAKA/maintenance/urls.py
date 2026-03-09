from django.urls import path
from maintenance import views

urlpatterns = [
    
    path('', views.list_urls),
    path('preventives/get/', views.maintenanceWithFiltering),
    path('preventives/add/', views.addPreventive),
    path('preventives/remove/', views.removePreventive),
]