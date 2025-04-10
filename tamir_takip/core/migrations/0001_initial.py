# Generated by Django 5.1.6 on 2025-03-20 19:01

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Arac',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marka', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('plaka', models.CharField(max_length=20, unique=True)),
                ('uretim_yili', models.IntegerField(default=2000)),
            ],
        ),
        migrations.CreateModel(
            name='IsEmri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aciklama', models.TextField()),
                ('durum', models.CharField(choices=[('beklemede', 'Beklemede'), ('incelemede', 'İncelemede'), ('onarim_sureci', 'Onarım Sürecinde'), ('test_asamasi', 'Test Aşamasında'), ('tamamlandi', 'Tamamlandı'), ('iptal_edildi', 'İptal Edildi')], default='beklemede', max_length=20)),
                ('oncelik', models.CharField(choices=[('normal', 'Normal'), ('yuksek', 'Yüksek'), ('acil', 'Acil')], default='normal', max_length=10)),
                ('baslama_tarihi', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Başlama Tarihi')),
                ('bitis_tarihi', models.DateTimeField(blank=True, null=True, verbose_name='Bitiş Tarihi')),
                ('olusturma_tarihi', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturma Tarihi')),
                ('yapilan_islemler', models.TextField(blank=True, verbose_name='Yapılan İşlemler')),
                ('kullanilan_parcalar', models.TextField(blank=True, verbose_name='Kullanılan Parçalar')),
                ('toplam_maliyet', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Toplam Maliyet')),
                ('kilometre', models.IntegerField(blank=True, null=True, verbose_name='Kilometre')),
                ('notlar', models.TextField(blank=True, verbose_name='Notlar')),
                ('arac', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='isemirleri', to='core.arac')),
                ('teknisyen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'İş Emri',
                'verbose_name_plural': 'İş Emirleri',
                'ordering': ['-baslama_tarihi'],
            },
        ),
        migrations.CreateModel(
            name='FaturaKalemi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kalem_tipi', models.CharField(choices=[('yedek_parca', 'Yedek Parça'), ('iscilik', 'İşçilik'), ('diger', 'Diğer')], max_length=50)),
                ('aciklama', models.CharField(max_length=255)),
                ('miktar', models.DecimalField(decimal_places=2, default=1, max_digits=10)),
                ('birim_fiyat', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_emri', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kalemler', to='core.isemri')),
            ],
            options={
                'ordering': ['kalem_tipi', 'id'],
            },
        ),
        migrations.CreateModel(
            name='IsEmriIslem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('islem_adi', models.CharField(max_length=100)),
                ('aciklama', models.TextField(blank=True)),
                ('tarih', models.DateTimeField(auto_now_add=True)),
                ('isemri', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='isemri_islemler', to='core.isemri')),
            ],
            options={
                'verbose_name': 'İş Emri İşlem',
                'verbose_name_plural': 'İş Emri İşlemleri',
            },
        ),
        migrations.CreateModel(
            name='IslemKaydi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('islem_tipi', models.CharField(choices=[('ariza_tespiti', 'Arıza Tespiti'), ('parca_siparisi', 'Parça Siparişi'), ('parca_degisimi', 'Parça Değişimi'), ('onarim', 'Onarım'), ('test', 'Test'), ('tamamlandi', 'Tamamlandı'), ('diger', 'Diğer')], max_length=50)),
                ('aciklama', models.TextField()),
                ('tarih', models.DateTimeField(auto_now_add=True)),
                ('is_emri', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='islemler', to='core.isemri')),
                ('teknisyen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-tarih'],
            },
        ),
        migrations.CreateModel(
            name='Musteri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad', models.CharField(max_length=255)),
                ('telefon', models.CharField(max_length=20)),
                ('adres', models.TextField()),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='arac',
            name='musteri',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.musteri'),
        ),
        migrations.CreateModel(
            name='Randevu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('randevu_tarihi', models.DateField()),
                ('randevu_saati', models.TimeField()),
                ('ariza_aciklamasi', models.TextField()),
                ('randevu_tipi', models.CharField(choices=[('bakim', 'Periyodik Bakım'), ('ariza', 'Arıza Tespiti/Onarım'), ('kaporta', 'Kaporta/Boya'), ('lastik', 'Lastik Değişimi'), ('diger', 'Diğer')], max_length=50)),
                ('iletisim_tercihi', models.CharField(choices=[('telefon', 'Telefon'), ('email', 'E-posta'), ('sms', 'SMS')], max_length=50)),
                ('durum', models.CharField(choices=[('beklemede', 'Beklemede'), ('onaylandi', 'Onaylandı'), ('iptal_edildi', 'İptal Edildi'), ('tamamlandi', 'Tamamlandı')], default='beklemede', max_length=50)),
                ('olusturulma_tarihi', models.DateTimeField(auto_now_add=True)),
                ('guncelleme_tarihi', models.DateTimeField(auto_now=True)),
                ('onay', models.BooleanField(default=False)),
                ('arac', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='randevular', to='core.arac')),
                ('musteri', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='randevular', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-randevu_tarihi', '-randevu_saati'],
            },
        ),
        migrations.CreateModel(
            name='TamirFotografi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fotograf', models.ImageField(upload_to='tamir_fotograflari/%Y/%m/')),
                ('aciklama', models.CharField(blank=True, max_length=255)),
                ('yukleme_tarihi', models.DateTimeField(auto_now_add=True)),
                ('is_emri', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fotograflar', to='core.isemri')),
            ],
            options={
                'ordering': ['-yukleme_tarihi'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('tamirci', 'Tamirci'), ('musteri', 'Müşteri')], default='musteri', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
