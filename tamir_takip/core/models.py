from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

# Author: K. Umut Araz
# Date: 02.03.2025


class UserProfile(models.Model):
    USER_TYPES = [
        ('tamirci', 'Tamirci'),
        ('musteri', 'Müşteri'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='musteri')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)
    instance.profile.save()


class Musteri(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    ad = models.CharField(max_length=255)
    telefon = models.CharField(max_length=20)
    adres = models.TextField()
    email = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.ad} - {self.telefon}"




class Arac(models.Model):
    musteri = models.ForeignKey(Musteri, on_delete=models.CASCADE)
    marka = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    plaka = models.CharField(max_length=20, unique=True)  
    uretim_yili = models.IntegerField()
    uretim_yili = models.IntegerField(default=2000)

    _son_isemri_cache = None
    
    @property
    def son_isemri(self):
        """Aracın en son iş emrini döndürür"""
        if self._son_isemri_cache is not None:
            return self._son_isemri_cache
        
        try:
            
            return self.isemirleri.order_by('-olusturma_tarihi').first()
        except AttributeError:
            try:
            
                return self.isemri_set.order_by('-olusturma_tarihi').first()
            except:
            
                return None
    
    @son_isemri.setter
    def son_isemri(self, value):
        """Son isemri için setter"""
        self._son_isemri_cache = value

    def __str__(self):
        return f"{self.marka} {self.model} ({self.plaka}) - {self.musteri.ad}"
    
    def get_son_isemri(self):
        """Aracın en son iş emrini döndürür"""
        try:
            return self.isemirleri.order_by('-olusturma_tarihi').first()
        except AttributeError:
            try:
                return self.isemri_set.order_by('-olusturma_tarihi').first()
            except:
                return None




class IsEmri(models.Model):
    DURUM_SECENEKLERI = (
        ('beklemede', 'Beklemede'),
        ('incelemede', 'İncelemede'),
        ('onarim_sureci', 'Onarım Sürecinde'),
        ('test_asamasi', 'Test Aşamasında'),
        ('tamamlandi', 'Tamamlandı'),
        ('iptal_edildi', 'İptal Edildi'),
    )
    
    ONCELIK_SECENEKLERI = [
        ('normal', 'Normal'),
        ('yuksek', 'Yüksek'),
        ('acil', 'Acil'),
    ]

    arac = models.ForeignKey('Arac', on_delete=models.CASCADE, related_name='isemirleri')
    aciklama = models.TextField()
    durum = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default='beklemede')
    oncelik = models.CharField(max_length=10, choices=ONCELIK_SECENEKLERI, default='normal')
    teknisyen = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    baslama_tarihi = models.DateTimeField(
        verbose_name="Başlama Tarihi",
        default=timezone.now
    )
    bitis_tarihi = models.DateTimeField(null=True, blank=True, verbose_name="Bitiş Tarihi")
    
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    
    yapilan_islemler = models.TextField(blank=True, verbose_name="Yapılan İşlemler")
    kullanilan_parcalar = models.TextField(blank=True, verbose_name="Kullanılan Parçalar")
    toplam_maliyet = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Toplam Maliyet")
    kilometre = models.IntegerField(null=True, blank=True, verbose_name="Kilometre")
    notlar = models.TextField(blank=True, verbose_name="Notlar")

    class Meta:
        ordering = ['-baslama_tarihi']
        verbose_name = "İş Emri"
        verbose_name_plural = "İş Emirleri"

    def __str__(self):
        return f"{self.arac.plaka} - {self.get_durum_display()} - {self.baslama_tarihi.strftime('%d.%m.%Y')}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.baslama_tarihi:
            from django.utils import timezone
            self.baslama_tarihi = timezone.now()
        
        if self.durum == 'tamamlandi' and not self.bitis_tarihi:
            from django.utils import timezone
            self.bitis_tarihi = timezone.now()
        super().save(*args, **kwargs)

    @property
    def durum_renk(self):
        """Duruma göre renk sınıfı döndürür"""
        renk_esleme = {
            'beklemede': 'warning',
            'incelemede': 'info',
            'onarim_sureci': 'primary',
            'test_asamasi': 'primary',
            'tamamlandi': 'success',
            'iptal_edildi': 'danger',
        }
        return renk_esleme.get(self.durum, 'secondary')
    
    @property
    def ara_toplam(self):
        """KDV hariç toplam tutarı hesaplar"""
        return sum(kalem.toplam_fiyat for kalem in self.kalemler.all())
    
    @property
    def kdv_tutari(self):
        """KDV tutarını hesaplar"""
        return self.ara_toplam * Decimal('0.18')  # %18 KDV
    
    @property
    def toplam_tutar(self):
        """KDV dahil toplam tutarı hesaplar"""
        return self.ara_toplam + self.kdv_tutari


class IsEmriIslem(models.Model):
    isemri = models.ForeignKey(IsEmri, on_delete=models.CASCADE, related_name='isemri_islemler')
    islem_adi = models.CharField(max_length=100)
    aciklama = models.TextField(blank=True)
    tarih = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "İş Emri İşlem"
        verbose_name_plural = "İş Emri İşlemleri"
        
    def __str__(self):
        return f"{self.isemri.id} - {self.islem_adi}"


class IslemKaydi(models.Model):
    ISLEM_TIPI_SECENEKLERI = (
        ('ariza_tespiti', 'Arıza Tespiti'),
        ('parca_siparisi', 'Parça Siparişi'),
        ('parca_degisimi', 'Parça Değişimi'),
        ('onarim', 'Onarım'),
        ('test', 'Test'),
        ('tamamlandi', 'Tamamlandı'),
        ('diger', 'Diğer'),
    )
    
    is_emri = models.ForeignKey(IsEmri, on_delete=models.CASCADE, related_name='islemler')
    islem_tipi = models.CharField(max_length=50, choices=ISLEM_TIPI_SECENEKLERI)
    aciklama = models.TextField()
    tarih = models.DateTimeField(auto_now_add=True)
    teknisyen = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-tarih']
    
    def __str__(self):
        return f"{self.get_islem_tipi_display()} - {self.tarih.strftime('%d.%m.%Y %H:%M')}"


class TamirFotografi(models.Model):
    is_emri = models.ForeignKey(IsEmri, on_delete=models.CASCADE, related_name='fotograflar')
    fotograf = models.ImageField(upload_to='tamir_fotograflari/%Y/%m/')
    aciklama = models.CharField(max_length=255, blank=True)
    yukleme_tarihi = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-yukleme_tarihi']
    
    def __str__(self):
        return f"Fotoğraf #{self.id} - İş Emri #{self.is_emri.id}"


class FaturaKalemi(models.Model):
    KALEM_TIPI_SECENEKLERI = (
        ('yedek_parca', 'Yedek Parça'),
        ('iscilik', 'İşçilik'),
        ('diger', 'Diğer'),
    )
    
    is_emri = models.ForeignKey(IsEmri, on_delete=models.CASCADE, related_name='kalemler')
    kalem_tipi = models.CharField(max_length=50, choices=KALEM_TIPI_SECENEKLERI)
    aciklama = models.CharField(max_length=255)
    miktar = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    birim_fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['kalem_tipi', 'id']
    
    def __str__(self):
        return f"{self.get_kalem_tipi_display()} - {self.aciklama}"
    
    @property
    def toplam_fiyat(self):
        return self.miktar * self.birim_fiyat


class Randevu(models.Model):
    RANDEVU_TIPI_SECENEKLERI = (
        ('bakim', 'Periyodik Bakım'),
        ('ariza', 'Arıza Tespiti/Onarım'),
        ('kaporta', 'Kaporta/Boya'),
        ('lastik', 'Lastik Değişimi'),
        ('diger', 'Diğer'),
    )
    
    ILETISIM_TERCIHI_SECENEKLERI = (
        ('telefon', 'Telefon'),
        ('email', 'E-posta'),
        ('sms', 'SMS'),
    )
    
    DURUM_SECENEKLERI = (
        ('beklemede', 'Beklemede'),
        ('onaylandi', 'Onaylandı'),
        ('iptal_edildi', 'İptal Edildi'),
        ('tamamlandi', 'Tamamlandı'),
    )
    
    musteri = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='randevular')
    arac = models.ForeignKey('Arac', on_delete=models.CASCADE, related_name='randevular')
    randevu_tarihi = models.DateField()
    randevu_saati = models.TimeField()
    ariza_aciklamasi = models.TextField()
    randevu_tipi = models.CharField(max_length=50, choices=RANDEVU_TIPI_SECENEKLERI)
    iletisim_tercihi = models.CharField(max_length=50, choices=ILETISIM_TERCIHI_SECENEKLERI)
    durum = models.CharField(max_length=50, choices=DURUM_SECENEKLERI, default='beklemede')
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)
    onay = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-randevu_tarihi', '-randevu_saati']
    
    def __str__(self):
        return f"{self.arac.musteri.ad} - {self.arac.plaka} - {self.randevu_tarihi}"
