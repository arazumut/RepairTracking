from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.routers import DefaultRouter
from .views import (
    home, musteri_list, arac_list, isemri_list, musteri_ekle,
    musteri_guncelle, musteri_sil, musteri_portal, tamir_durum,
    MusteriViewSet, AracViewSet, IsEmriViewSet, register, arac_ekle, isemri_ekle,
    arac_duzenle, arac_sil, isemri_duzenle, isemri_sil, arac_detay, musteri_detay,
    logout_view, login_view, HomeView, welcome, musteri_arac_ekle, musteri_arac_list, musteri_isemri_list,
    musteri_isemri_ekle, musteri_isemri_detay, musteri_isemri_iptal
)
from django.contrib.auth.decorators import login_required, user_passes_test


def is_tamirci(user):
    return hasattr(user, 'profile') and user.profile.user_type == 'tamirci'

tamirci_required = user_passes_test(is_tamirci, login_url='musteri_portal')

router = DefaultRouter()
router.register(r'musteriler', MusteriViewSet)
router.register(r'araclar', AracViewSet)
router.register(r'isemirleri', IsEmriViewSet)


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', login_required(tamirci_required(HomeView.as_view())), name='home'),
    path('register/', views.register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('musteriler/', login_required(tamirci_required(musteri_list)), name='musteri_list'),
    path('musteri-ekle/', login_required(tamirci_required(musteri_ekle)), name='musteri_ekle'),
    path('musteri-guncelle/<int:pk>/', login_required(tamirci_required(musteri_guncelle)), name='musteri_guncelle'),
    path('musteri-sil/<int:pk>/', login_required(tamirci_required(musteri_sil)), name='musteri_sil'),
    path('musteri/<int:pk>/detay/', login_required(tamirci_required(musteri_detay)), name='musteri_detay'),

    path('araclar/', login_required(tamirci_required(arac_list)), name='arac_list'),
    path('arac-ekle/', login_required(tamirci_required(arac_ekle)), name='arac_ekle'),
    path('arac/<int:pk>/duzenle/', login_required(tamirci_required(arac_duzenle)), name='arac_duzenle'),
    path('arac/<int:pk>/sil/', login_required(tamirci_required(arac_sil)), name='arac_sil'),
    path('arac/<int:pk>/detay/', login_required(arac_detay), name='arac_detay'),
    
    path('isemirleri/', login_required(tamirci_required(isemri_list)), name='isemri_list'),
    path('isemri-ekle/', login_required(tamirci_required(isemri_ekle)), name='isemri_ekle'),
    path('isemri/<int:pk>/duzenle/', login_required(tamirci_required(isemri_duzenle)), name='isemri_duzenle'),
    path('isemri/<int:pk>/sil/', login_required(tamirci_required(isemri_sil)), name='isemri_sil'),

    path('musteri-portal/', login_required(musteri_portal), name='musteri_portal'),
    path('musteri-arac-ekle/', views.musteri_arac_ekle, name='musteri_arac_ekle'),
    path('musteri-araclar/', login_required(musteri_arac_list), name='musteri_arac_list'),
    path('musteri-isemirleri/', views.musteri_isemri_list, name='musteri_isemri_list'),
    path('musteri-isemri-ekle/', views.musteri_isemri_ekle, name='musteri_isemri_ekle'),
    path('musteri-isemri/<int:isemri_id>/', views.musteri_isemri_detay, name='musteri_isemri_detay'),
    path('musteri-isemri/<int:isemri_id>/iptal/', views.musteri_isemri_iptal, name='musteri_isemri_iptal'),
    path('tamir-durum/<int:pk>/', login_required(tamir_durum), name='tamir_durum'),

    path('api/', include(router.urls)),
    path('iletisim/', views.iletisim, name='iletisim'),
]
