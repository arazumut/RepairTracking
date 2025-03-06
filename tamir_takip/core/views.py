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
#anasayfa
#müşteri portalı
#tamir durum


from django.shortcuts import render
from .models import Musteri
from django.shortcuts import render, redirect
from .forms import MusteriForm, AracForm, IsEmriForm
from .models import IsEmri
from .models import Arac
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from rest_framework import viewsets
from .models import Musteri, Arac, IsEmri
from .serializers import MusteriSerializer, AracSerializer, IsEmriSerializer
from django.db.models import Q 
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"


# telefondan çalıştıracakken veya başka ortamda LOGİN RQUIRED KALDIR!

def home(request):
    return render(request, 'core/home.html')



def musteri_portal(request):
    musteriler = Musteri.objects.filter(user=request.user)
    return render(request, 'core/musteri_portal.html', {'musteriler': musteriler})


def tamir_durum(request, pk):
    is_emri = get_object_or_404(IsEmri, pk=pk)
    return render(request, 'core/tamir_durum.html', {'is_emri': is_emri})



def musteri_list(request):
    musteriler = Musteri.objects.all()
    return render(request, "core/musteri_list.html", {"musteriler": musteriler})


def arac_list(request):
    araclar = Arac.objects.all()
    return render(request, "core/arac_list.html", {"araclar": araclar})


def isemri_list(request):
    is_emirleri = IsEmri.objects.all()
    return render(request, "core/isemri_list.html", {"is_emirleri": is_emirleri})



from .forms import MusteriForm, AracForm

from django.shortcuts import render, redirect
from .forms import MusteriForm
from .models import Musteri, Arac, IsEmri



def musteri_ekle(request):
    if request.method == "POST":
        form = MusteriForm(request.POST)
        if form.is_valid():
            
            musteri = form.save()

            
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


def arac_ekle(request):
    if request.method == "POST":
        form = AracForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('arac_list')
    else:
        form = AracForm()
    return render(request, 'core/arac_form.html', {'form': form})



def isemri_ekle(request):
    if request.method == "POST":
        form = IsEmriForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('isemri_list')
    else:
        form = IsEmriForm()
    return render(request, 'core/isemri_form.html', {'form': form})

def arac_duzenle(request, pk):
    arac = get_object_or_404(Arac, pk=pk)
    if request.method == "POST":
        form = AracForm(request.POST, instance=arac)
        if form.is_valid():
            form.save()
            return redirect('arac_list')
    else:
        form = AracForm(instance=arac)
    return render(request, 'core/arac_form.html', {'form': form})

def arac_sil(request, pk):
    arac = get_object_or_404(Arac, pk=pk)
    if request.method == "POST":
        arac.delete()
        return redirect('arac_list')
    return render(request, 'core/arac_sil.html', {'arac': arac})

def isemri_duzenle(request, pk):
    isemri = get_object_or_404(IsEmri, pk=pk)
    if request.method == "POST":
        form = IsEmriForm(request.POST, instance=isemri)
        if form.is_valid():
            form.save()
            return redirect('isemri_list')
    else:
        form = IsEmriForm(instance=isemri)
    return render(request, 'core/isemri_form.html', {'form': form})

def isemri_sil(request, pk):
    isemri = get_object_or_404(IsEmri, pk=pk)
    if request.method == "POST":
        isemri.delete()
        return redirect('isemri_list')
    return render(request, 'core/isemri_sil.html', {'isemri': isemri})




