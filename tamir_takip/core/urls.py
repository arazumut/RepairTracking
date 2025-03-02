from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, musteri_list, arac_list, isemri_list, musteri_ekle, musteri_guncelle, musteri_sil

urlpatterns = [

    path('', home, name='home'),
    
    
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    
    path('musteriler/', musteri_list, name='musteri_list'),  
    path('musteri-ekle/', musteri_ekle, name='musteri_ekle'),  
    path('musteri-guncelle/<int:pk>/', musteri_guncelle, name='musteri_guncelle'),  
    path('musteri-sil/<int:pk>/', musteri_sil, name='musteri_sil'),  
    
    
    path('araclar/', arac_list, name='arac_list'),
    path('isemirleri/', isemri_list, name='isemri_list'),  
]