from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import (
    home, musteri_list, arac_list, isemri_list, musteri_ekle,
    musteri_guncelle, musteri_sil, musteri_portal, tamir_durum,
    MusteriViewSet, AracViewSet, IsEmriViewSet, register,  # Kayıt fonksiyonu eklendi
    arac_guncelle,  # Arac güncelleme fonksiyonunu ekleyin
    arac_sil,  # Arac silme fonksiyonunu ekleyin
    isemri_guncelle,  # İş emri güncelleme fonksiyonunu ekleyin
    isemri_sil,  
)


router = DefaultRouter()
router.register(r'musteriler', MusteriViewSet)
router.register(r'araclar', AracViewSet)
router.register(r'isemirleri', IsEmriViewSet)


urlpatterns = [
    path('', home, name='home'),

    
    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    
    path('musteriler/', musteri_list, name='musteri_list'),
    path('musteri-ekle/', musteri_ekle, name='musteri_ekle'),
    path('musteri-guncelle/<int:pk>/', musteri_guncelle, name='musteri_guncelle'),
    path('musteri-sil/<int:pk>/', musteri_sil, name='musteri_sil'),


    path('araclar/', arac_list, name='arac_list'),
    path('arac-guncelle/<int:pk>/', arac_guncelle, name='arac_guncelle'),  
    path('arac-sil/<int:pk>/', arac_sil, name='arac_sil'),  
    path('isemirleri/', isemri_list, name='isemri_list'),
    path('isemri-guncelle/<int:pk>/', isemri_guncelle, name='isemri_guncelle'),  
    path('isemri-sil/<int:pk>/', isemri_sil, name='isemri_sil'), 

    
    path('musteri-portal/', musteri_portal, name='musteri_portal'),
    path('tamir-durum/<int:pk>/', tamir_durum, name='tamir_durum'),

    
    path('register/', register, name='register'),


    path('api/', include(router.urls)),
]
