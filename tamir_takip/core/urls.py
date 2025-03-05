from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    home, musteri_list, arac_list, isemri_list, musteri_ekle,
    musteri_guncelle, musteri_sil, musteri_portal, tamir_durum,
    MusteriViewSet, AracViewSet, IsEmriViewSet,
    arac_guncelle, arac_sil, arac_ekle,
    isemri_guncelle, isemri_sil, isemri_ekle,
    musteri_detay, arac_detay
)

router = DefaultRouter()
router.register(r'musteriler', MusteriViewSet)
router.register(r'araclar', AracViewSet)
router.register(r'isemirleri', IsEmriViewSet)

urlpatterns = [
    path('', home, name='home'),
    
    path('musteriler/', musteri_list, name='musteri_list'),
    path('musteri-ekle/', musteri_ekle, name='musteri_ekle'),
    path('musteri-detay/<int:pk>/', musteri_detay, name='musteri_detay'),
    path('musteri-guncelle/<int:pk>/', musteri_guncelle, name='musteri_guncelle'),
    path('musteri-sil/<int:pk>/', musteri_sil, name='musteri_sil'),

    path('araclar/', arac_list, name='arac_list'),
    path('arac-ekle/', arac_ekle, name='arac_ekle'),
    path('arac-detay/<int:pk>/', arac_detay, name='arac_detay'),
    path('arac-guncelle/<int:pk>/', arac_guncelle, name='arac_guncelle'),
    path('arac-sil/<int:pk>/', arac_sil, name='arac_sil'),
    
    path('isemirleri/', isemri_list, name='isemri_list'),
    path('isemri-ekle/', isemri_ekle, name='isemri_ekle'),
    path('isemri-guncelle/<int:pk>/', isemri_guncelle, name='isemri_guncelle'),
    path('isemri-sil/<int:pk>/', isemri_sil, name='isemri_sil'),
    
    path('tamir-durum/<int:pk>/', tamir_durum, name='tamir_durum'),

    path('api/', include(router.urls)),
]
