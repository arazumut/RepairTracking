# Generated by Django 5.1.6 on 2025-03-05 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_musteri_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='isemri',
            name='baslama_tarihi',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
