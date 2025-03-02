from django.db import models
from django.contrib.auth.models import User


class Musteri(models.Model):
    ad = models.CharField(max_length=255)
    telefon = models.CharField(max_length=20)
    adres = models.TextField()

    def __str__(self):
        return self.ad


class Arac(models.Model):
    musteri = models.ForeignKey(Musteri, on_delete=models.CASCADE)
    marka = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    plaka = models.CharField(max_length=20, unique=True)
    uretim_yili = models.IntegerField()

    def __str__(self):
        return f"{self.marka} {self.model} ({self.plaka})"


class IsEmri(models.Model):
    DURUM_SECENEKLERI = [
        ('beklemede', 'Beklemede'),
        ('inceleniyor', 'İnceleniyor'),
        ('tamirde', 'Tamirde'),
        ('tamamlandi', 'Tamamlandı'),
    ]

    arac = models.ForeignKey(Arac, on_delete=models.CASCADE)
    aciklama = models.TextField()
    durum = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default='beklemede')
    teknisyen = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    baslama_tarihi = models.DateTimeField(auto_now_add=True)
    bitis_tarihi = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"İş Emri: {self.arac} - {self.durum}"
