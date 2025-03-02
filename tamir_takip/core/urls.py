from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, musteri_list, arac_list, isemri_list, musteri_ekle, musteri_guncelle, musteri_sil

urlpatterns = [
    # Anasayfa
    path('', home, name='home'),
    
    # Kullanıcı giriş ve çıkış işlemleri
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Müşteri işlemleri
    path('musteriler/', musteri_list, name='musteri_list'),  # Müşteri listesi
    path('musteri-ekle/', musteri_ekle, name='musteri_ekle'),  # Müşteri ekle
    path('musteri-guncelle/<int:pk>/', musteri_guncelle, name='musteri_guncelle'),  # Müşteri güncelle
    path('musteri-sil/<int:pk>/', musteri_sil, name='musteri_sil'),  # Müşteri sil
    
    # Araç işlemleri
    path('araclar/', arac_list, name='arac_list'),  # Araç listesi

    # İş emri işlemleri
    path('isemirleri/', isemri_list, name='isemri_list'),  # İş emirleri listesi
]