from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, musteri_list, arac_list, isemri_list, musteri_ekle, musteri_guncelle, musteri_sil

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MusteriViewSet, AracViewSet, IsEmriViewSet

#router ile api yönlendrme yapılır bunu unutma
router = DefaultRouter()
router.register(r'musteriler', MusteriViewSet)
router.register(r'araclar', AracViewSet)
router.register(r'isemirleri', IsEmriViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  
]


urlpatterns = [

    path('', home, name='home'),
    
    #login ve logout sayfa yolları
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    #müşteri işlemleri sayfa yollarımız bu şekilde sınıf sınıf yap kafa karışıklığı olmasın
    path('musteriler/', musteri_list, name='musteri_list'),  
    path('musteri-ekle/', musteri_ekle, name='musteri_ekle'),  
    path('musteri-guncelle/<int:pk>/', musteri_guncelle, name='musteri_guncelle'),  
    path('musteri-sil/<int:pk>/', musteri_sil, name='musteri_sil'),  
    
    #araç işlemleri sayfa yollarımız bu şekilde.
    path('araclar/', arac_list, name='arac_list'),
    path('isemirleri/', isemri_list, name='isemri_list'),  
]