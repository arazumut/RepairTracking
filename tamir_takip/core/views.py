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
from .models import Musteri, UserProfile
from django.shortcuts import render, redirect
from .forms import MusteriForm, AracForm, IsEmriForm, UserRegisterForm
from .models import IsEmri
from .models import Arac
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from rest_framework import viewsets
from .models import Musteri, Arac, IsEmri
from .serializers import MusteriSerializer, AracSerializer, IsEmriSerializer
from django.db.models import Q 
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django import forms
from django.contrib import messages

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['musteri_sayisi'] = Musteri.objects.count()
        context['arac_sayisi'] = Arac.objects.count()
        context['isemri_sayisi'] = IsEmri.objects.count()
        context['son_is_emirleri'] = IsEmri.objects.all().order_by('-baslama_tarihi')[:5]
        return context


def welcome(request):
    return render(request, 'core/welcome.html')


# telefondan çalıştıracakken veya başka ortamda LOGİN RQUIRED KALDIR!

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'core/welcome.html')
    
    # Giriş yapmış kullanıcılar için
    if hasattr(request.user, 'profile') and request.user.profile.user_type == 'musteri':
        return redirect('musteri_portal')
    
    # Tamirci kullanıcılar için dashboard
    musteri_sayisi = Musteri.objects.count()
    arac_sayisi = Arac.objects.count()
    isemri_sayisi = IsEmri.objects.count()
    
    return render(request, 'core/home.html', {
        'musteri_sayisi': musteri_sayisi,
        'arac_sayisi': arac_sayisi,
        'isemri_sayisi': isemri_sayisi
    })



def musteri_portal(request):
    # Kullanıcıya bağlı müşteri kaydını bul
    try:
        musteri = Musteri.objects.get(user=request.user)
        # Müşteriye ait araçları getir
        araclar = Arac.objects.filter(musteri=musteri)
        
        # Araçlara ait iş emirlerini getir
        is_emirleri = {}
        for arac in araclar:
            is_emirleri[arac.id] = IsEmri.objects.filter(arac=arac).order_by('-baslama_tarihi')
        
        context = {
            'musteri': musteri,
            'araclar': araclar,
            'is_emirleri': is_emirleri,
        }
        
        return render(request, 'core/musteri_portal.html', context)
    except Musteri.DoesNotExist:
        # Eğer kullanıcıya bağlı müşteri kaydı yoksa, yeni kayıt oluşturma formu göster
        if request.method == "POST":
            form = MusteriForm(request.POST)
            if form.is_valid():
                musteri = form.save(commit=False)
                musteri.user = request.user
                musteri.save()
                messages.success(request, 'Müşteri bilgileriniz başarıyla kaydedildi.')
                return redirect('musteri_portal')
        else:
            form = MusteriForm()
        
        return render(request, 'core/musteri_form.html', {
            'form': form, 
            'title': 'Müşteri Bilgilerinizi Tamamlayın',
            'is_portal': True
        })


@login_required
def tamir_durum(request, pk):
    is_emri = get_object_or_404(IsEmri, pk=pk)
    
    # Kullanıcının kendi aracına ait iş emri olup olmadığını kontrol et
    if hasattr(request.user, 'profile') and request.user.profile.user_type == 'musteri':
        try:
            musteri = Musteri.objects.get(user=request.user)
            if is_emri.arac.musteri != musteri:
                messages.error(request, 'Bu iş emrine erişim izniniz bulunmamaktadır.')
                return redirect('musteri_portal')
        except Musteri.DoesNotExist:
            messages.error(request, 'Müşteri bilgileriniz bulunamadı.')
            return redirect('musteri_portal')
    
    # İş emrine ait notları getir (eğer bir notlar modeli varsa)
    # notlar = IsEmriNotu.objects.filter(is_emri=is_emri).order_by('-tarih')
    
    context = {
        'is_emri': is_emri,
        # 'notlar': notlar
    }
    
    return render(request, 'core/tamir_durum.html', context)



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
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Müşteri tipindeki kullanıcılar için müşteri portalına yönlendir
            if user.profile.user_type == 'musteri':
                return redirect('musteri_portal')
            return redirect('home')
    else:
        form = UserRegisterForm()
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

def arac_detay(request, pk):
    arac = get_object_or_404(Arac, pk=pk)
    isemri_listesi = IsEmri.objects.filter(arac=arac).order_by('-baslama_tarihi')
    context = {
        'arac': arac,
        'isemri_listesi': isemri_listesi
    }
    return render(request, 'core/arac_detay.html', context)

def musteri_detay(request, pk):
    musteri = get_object_or_404(Musteri, pk=pk)
    araclar = Arac.objects.filter(musteri=musteri).prefetch_related('is_emirleri')
    
    if request.method == "POST":
        form = AracForm(request.POST)
        if form.is_valid():
            arac = form.save(commit=False)
            arac.musteri = musteri
            arac.save()
            return redirect('musteri_detay', pk=musteri.pk)
    else:
        form = AracForm(initial={'musteri': musteri})
        form.fields['musteri'].widget = forms.HiddenInput()
    
    context = {
        'musteri': musteri,
        'araclar': araclar,
        'form': form
    }
    return render(request, 'core/musteri_detay.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('welcome')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Başarıyla giriş yaptınız.')
            
            # Kullanıcı tipine göre yönlendirme
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.user_type == 'musteri':
                    return redirect('musteri_portal')
                else:
                    return redirect('home')
            except UserProfile.DoesNotExist:
                return redirect('home')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
    
    return render(request, 'core/login.html')

@login_required
def musteri_arac_ekle(request):
    """Müşteri portalından araç ekleme view'i"""
    if request.method == "POST":
        try:
            musteri = Musteri.objects.get(user=request.user)
            
    
            marka = request.POST.get('marka')
            model = request.POST.get('model')
            plaka = request.POST.get('plaka')
            uretim_yili = request.POST.get('uretim_yili')
            sorun_aciklama = request.POST.get('sorun_aciklama')
            
            
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
                messages.success(request, f'{marka} {model} aracınız ve ilgili iş emri başarıyla oluşturuldu.')
            else:
                messages.success(request, f'{marka} {model} aracınız başarıyla eklendi.')
                
            return redirect('musteri_portal')
            
        except Musteri.DoesNotExist:
            messages.error(request, 'Müşteri bilgileriniz bulunamadı.')
            return redirect('musteri_portal')
    
    # GET isteği için müşteri portalına yönlendir
    return redirect('musteri_portal')




