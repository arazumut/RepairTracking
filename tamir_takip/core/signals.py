from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Musteri, Arac, IsEmri

@receiver(post_save, sender=Musteri)
def otomatik_arac_ve_isemri_ekle(sender, instance, created, **kwargs):
    if created:
        arac = create_default_arac(instance)
        create_default_isemri(instance, arac)

def create_default_arac(musteri):
    return Arac.objects.create(
        musteri=musteri,
        marka="Bilinmiyor",
        model="Bilinmiyor",
        plaka=f"XX-{musteri.id:04d}",
    )

def create_default_isemri(musteri, arac):
    return IsEmri.objects.create(
        musteri=musteri,
        arac=arac,
        aciklama="Otomatik oluşturulan iş emri",
        durum="Beklemede"
    )