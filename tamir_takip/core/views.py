from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from rest_framework import viewsets

from .models import Musteri, Arac, IsEmri
from .forms import MusteriForm, AracForm, IsEmriForm
from .serializers import MusteriSerializer, AracSerializer, IsEmriSerializer

class MusteriViewSet(viewsets.ModelViewSet):
    queryset = Musteri.objects.all()
    serializer_class = MusteriSerializer

class AracViewSet(viewsets.ModelViewSet):
    queryset = Arac.objects.all()
    serializer_class = AracSerializer

class IsEmriViewSet(viewsets.ModelViewSet):
    queryset = IsEmri.objects.all()
    serializer_class = IsEmriSerializer

def home(request):
    return render(request, 'core/home.html')

def musteri_portal(request):
    try:
        musteri = Musteri.objects.first()  
        araclar = Arac.objects.filter(musteri=musteri)
        is_emirleri = IsEmri.objects.filter(arac__musteri=musteri)
        return render(request, 'core/musteri_portal.html', {
            'musteri': musteri,
            'araclar': araclar,
            'is_emirleri': is_emirleri
        })
    except Musteri.DoesNotExist:
        messages.error(request, 'Müşteri bilgileri bulunamadı.')
        return redirect('home')

def musteri_list(request):
    query = request.GET.get("q", "")
    musteriler = Musteri.objects.filter(Q(ad__icontains=query))
    return render(request, "core/musteri_list.html", {"musteriler": musteriler, "q": query})

def arac_list(request):
    query = request.GET.get("q", "")
    araclar = Arac.objects.filter(Q(plaka__icontains=query))
    return render(request, "core/arac_list.html", {"araclar": araclar, "q": query})

def isemri_list(request):
    is_emirleri = IsEmri.objects.all()
    durum = request.GET.get("durum", "")
    if durum:
        is_emirleri = is_emirleri.filter(durum=durum)
    return render(request, "core/isemri_list.html", {"is_emirleri": is_emirleri, "durum": durum})

def musteri_ekle(request):
    if request.method == "POST":
        form = MusteriForm(request.POST)
        if form.is_valid():
            musteri = form.save()
            
            # Araç bilgilerini al
            marka = form.cleaned_data.get('marka')
            model = form.cleaned_data.get('model')
            plaka = form.cleaned_data.get('plaka')
            uretim_yili = form.cleaned_data.get('uretim_yili')
            sorun_aciklama = form.cleaned_data.get('sorun_aciklama')
            
            # Eğer araç bilgileri varsa araç oluştur
            if marka and model and plaka and uretim_yili:
                arac = Arac.objects.create(
                    musteri=musteri,
                    marka=marka,
                    model=model,
                    plaka=plaka,
                    uretim_yili=uretim_yili
                )
                
                # Eğer sorun açıklaması varsa iş emri oluştur
                if sorun_aciklama:
                    IsEmri.objects.create(
                        arac=arac,
                        aciklama=sorun_aciklama,
                        durum="beklemede"
                    )
            
            messages.success(request, 'Müşteri başarıyla eklendi.')
            return redirect('musteri_list')
    else:
        form = MusteriForm()
    
    return render(request, 'core/musteri_form.html', {'form': form})

def musteri_guncelle(request, pk):
    musteri = get_object_or_404(Musteri, id=pk)
    if request.method == "POST":
        form = MusteriForm(request.POST, instance=musteri)
        if form.is_valid():
            form.save()
            return redirect('musteri_list')
    else:
        form = MusteriForm(instance=musteri)
    return render(request, 'core/musteri_form.html', {'form': form})

def musteri_sil(request, pk):
    musteri = get_object_or_404(Musteri, id=pk)
    if request.method == "POST":
        musteri.delete()
        return redirect('musteri_list')
    return render(request, 'core/musteri_sil.html', {'musteri': musteri})

def arac_ekle(request):
    if request.method == "POST":
        form = AracForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('arac_list')
    else:
        form = AracForm()
    
    return render(request, 'core/arac_form.html', {'form': form})

def arac_guncelle(request, pk):
    arac = get_object_or_404(Arac, pk=pk)
    if request.method == "POST":
        form = AracForm(request.POST, instance=arac)
        if form.is_valid():
            form.save()
            return redirect('arac_list')
    else:
        form = AracForm(instance=arac)
    return render(request, 'core/arac_guncelle.html', {'form': form})

def arac_sil(request, pk):
    arac = get_object_or_404(Arac, pk=pk)
    if request.method == "POST":
        arac.delete()
        return redirect('arac_list')
    return render(request, 'core/arac_sil.html', {'arac': arac})

def isemri_guncelle(request, pk):
    is_emri = get_object_or_404(IsEmri, pk=pk)
    if request.method == "POST":
        form = IsEmriForm(request.POST, instance=is_emri)
        if form.is_valid():
            form.save()
            return redirect('isemri_list')
    else:
        form = IsEmriForm(instance=is_emri)
    return render(request, 'core/isemri_guncelle.html', {'form': form})

def isemri_sil(request, pk):
    is_emri = get_object_or_404(IsEmri, pk=pk)
    if request.method == "POST":
        is_emri.delete()
        return redirect('isemri_list')
    return render(request, 'core/isemri_sil.html', {'is_emri': is_emri})

def tamir_durum(request, pk):
    try:
        musteri = Musteri.objects.get(id=pk)
        araclar = Arac.objects.filter(musteri=musteri)
        is_emirleri = IsEmri.objects.filter(arac__musteri=musteri)
        return render(request, 'core/tamir_durum.html', {
            'musteri': musteri,
            'araclar': araclar,
            'is_emirleri': is_emirleri
        })
    except Musteri.DoesNotExist:
        messages.error(request, 'Müşteri bulunamadı.')
        return redirect('musteri_list')

def isemri_ekle(request):
    if request.method == "POST":
        form = IsEmriForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('isemri_list')
    else:
        form = IsEmriForm()
    
    return render(request, 'core/isemri_form.html', {'form': form})

def musteri_detay(request, pk):
    musteri = get_object_or_404(Musteri, pk=pk)
    araclar = Arac.objects.filter(musteri=musteri)
    is_emirleri = IsEmri.objects.filter(arac__musteri=musteri)
    return render(request, 'core/musteri_detay.html', {
        'musteri': musteri,
        'araclar': araclar,
        'is_emirleri': is_emirleri
    })

def arac_detay(request, pk):
    arac = get_object_or_404(Arac, pk=pk)
    is_emirleri = IsEmri.objects.filter(arac=arac)
    return render(request, 'core/arac_detay.html', {
        'arac': arac,
        'is_emirleri': is_emirleri
    })
