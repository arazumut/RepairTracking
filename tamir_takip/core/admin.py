from django.contrib import admin
from .models import Musteri, Arac, IsEmri

@admin.register(Musteri)
class MusteriAdmin(admin.ModelAdmin):
    list_display = ('ad', 'telefon', 'email')
    search_fields = ('ad', 'telefon', 'email')

@admin.register(Arac)
class AracAdmin(admin.ModelAdmin):
    list_display = ('marka', 'model', 'plaka', 'musteri')
    search_fields = ('marka', 'model', 'plaka', 'musteri__ad')

@admin.register(IsEmri)
class IsEmriAdmin(admin.ModelAdmin):
    list_display = ('arac', 'durum', 'baslama_tarihi', 'bitis_tarihi')
    list_filter = ('durum',)
    search_fields = ('arac__marka', 'arac__model', 'arac__plaka')