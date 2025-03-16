from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.routers import DefaultRouter
from .views import (
    home, musteri_list, arac_list, isemri_list, musteri_ekle,
    musteri_guncelle, musteri_sil, musteri_portal, tamir_durum,
    MusteriViewSet, AracViewSet, IsEmriViewSet, register, arac_ekle, isemri_ekle,
    arac_duzenle, arac_sil, isemri_duzenle, isemri_sil, arac_detay, musteri_detay,
    logout_view, login_view, HomeView, welcome, musteri_arac_ekle
)
from django.contrib.auth.decorators import login_required


router = DefaultRouter()
router.register(r'musteriler', MusteriViewSet)
router.register(r'araclar', AracViewSet)
router.register(r'isemirleri', IsEmriViewSet)


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', HomeView.as_view(), name='home'),
    path('register/', views.register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Tamirci erişimi gerektiren URL'ler
    path('musteriler/', musteri_list, name='musteri_list'),
    path('musteri-ekle/', musteri_ekle, name='musteri_ekle'),
    path('musteri-guncelle/<int:pk>/', musteri_guncelle, name='musteri_guncelle'),
    path('musteri-sil/<int:pk>/', musteri_sil, name='musteri_sil'),
    path('musteri/<int:pk>/detay/', musteri_detay, name='musteri_detay'),

    path('araclar/', arac_list, name='arac_list'),
    path('arac-ekle/', arac_ekle, name='arac_ekle'),
    path('arac/<int:pk>/duzenle/', arac_duzenle, name='arac_duzenle'),
    path('arac/<int:pk>/sil/', arac_sil, name='arac_sil'),
    path('arac/<int:pk>/detay/', arac_detay, name='arac_detay'),
    
    path('isemirleri/', isemri_list, name='isemri_list'),
    path('isemri-ekle/', isemri_ekle, name='isemri_ekle'),
    path('isemri/<int:pk>/duzenle/', isemri_duzenle, name='isemri_duzenle'),
    path('isemri/<int:pk>/sil/', isemri_sil, name='isemri_sil'),

    # Müşteri erişimi olan URL'ler
    path('musteri-portal/', musteri_portal, name='musteri_portal'),
    path('musteri-arac-ekle/', musteri_arac_ekle, name='musteri_arac_ekle'),
    path('tamir-durum/<int:pk>/', tamir_durum, name='tamir_durum'),

    # API URL'leri
    path('api/', include(router.urls)),
]
