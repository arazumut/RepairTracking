#Author: K. Umut Araz
#Date: 02.03.2025

#tamir_takip/core/views.py
#Modelleri tanımla
#login istensin
#müşteri listesi
#araç listesi
#iş emri listesi
#müşteri ekle
#müşteri güncelle
#müşteri sil
#kullanıcı kayıt
#api viewsetler


from django.shortcuts import render
from .models import Musteri
from django.shortcuts import render, redirect
from .forms import MusteriForm
from .models import IsEmri
from .models import Arac
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from rest_framework import viewsets
from .models import Musteri, Arac, IsEmri
from .serializers import MusteriSerializer, AracSerializer, IsEmriSerializer

@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def musteri_list(request):
    musteriler = Musteri.objects.all()
    return render(request, 'core/musteri_list.html', {'musteriler': musteriler})

@login_required
def arac_list(request):
    araclar = Arac.objects.all()
    return render(request, 'core/arac_list.html', {'araclar': araclar})


@login_required
def isemri_list(request):
    is_emirleri = IsEmri.objects.all()
    return render(request, 'core/isemri_list.html', {'is_emirleri': is_emirleri})


from .forms import MusteriForm, AracForm

from django.shortcuts import render, redirect
from .forms import MusteriForm
from .models import Musteri, Arac, IsEmri



def musteri_ekle(request):
    if request.method == "POST":
        form = MusteriForm(request.POST)
        if form.is_valid():
            # 1️⃣ Müşteriyi Kaydet
            musteri = form.save()

            # 2️⃣ Araç Bilgilerini Kaydet
            arac = Arac.objects.create(
                musteri=musteri,
                marka=form.cleaned_data['marka'],
                model=form.cleaned_data['model'],
                plaka=form.cleaned_data['plaka'],
                uretim_yili=form.cleaned_data['uretim_yili']
            )

            
            IsEmri.objects.create(
                arac=arac,
                aciklama=form.cleaned_data['sorun_aciklama'],
                durum="beklemede"
            )

            return redirect('musteri_list')
    else:
        form = MusteriForm()

    return render(request, 'core/musteri_form.html', {'form': form})




def musteri_guncelle(request, pk):
    musteri = Musteri.objects.get(id=pk)
    if request.method == "POST":
        form = MusteriForm(request.POST, instance=musteri)
        if form.is_valid():
            form.save()
            return redirect('musteri_list')
    else:
        form = MusteriForm(instance=musteri)
    return render(request, 'core/musteri_form.html', {'form': form})


def musteri_sil(request, pk):
    musteri = Musteri.objects.get(id=pk)
    if request.method == "POST":
        musteri.delete()
        return redirect('musteri_list')
    return render(request, 'core/musteri_sil.html', {'musteri': musteri})



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')  
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})




class MusteriViewSet(viewsets.ModelViewSet):
    queryset = Musteri.objects.all()
    serializer_class = MusteriSerializer

class AracViewSet(viewsets.ModelViewSet):
    queryset = Arac.objects.all()
    serializer_class = AracSerializer

class IsEmriViewSet(viewsets.ModelViewSet):
    queryset = IsEmri.objects.all()
    serializer_class = IsEmriSerializer





