from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    def __str__(self):
        return f"{self.marka} {self.model} ({self.plaka}) - {self.musteri.ad}"
    



class IsEmri(models.Model):
    DURUM_SECENEKLERI = [
        ('beklemede', 'Beklemede'),
        ('inceleniyor', 'İnceleniyor'),
        ('tamirde', 'Tamirde'),
        ('tamamlandi', 'Tamamlandı'),
    ]
    
    ONCELIK_SECENEKLERI = [
        ('normal', 'Normal'),
        ('yuksek', 'Yüksek'),
        ('acil', 'Acil'),
    ]

    arac = models.ForeignKey(Arac, on_delete=models.CASCADE, related_name='is_emirleri')
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


class IsEmriIslem(models.Model):
    isemri = models.ForeignKey(IsEmri, on_delete=models.CASCADE, related_name='islemler')
    islem_adi = models.CharField(max_length=100)
    aciklama = models.TextField(blank=True)
    tarih = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "İş Emri İşlem"
        verbose_name_plural = "İş Emri İşlemleri"
        
    def __str__(self):
        return f"{self.isemri.id} - {self.islem_adi}"
