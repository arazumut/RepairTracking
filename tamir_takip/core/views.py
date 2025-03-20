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
from .forms import MusteriForm, AracForm, IsEmriForm, UserRegisterForm, RandevuForm
from .models import IsEmri
from .models import Arac
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from rest_framework import viewsets
from .models import Musteri, Arac, IsEmri, IsEmriIslem
from .serializers import MusteriSerializer, AracSerializer, IsEmriSerializer
from django.db.models import Q 
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django import forms
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, Http404
from .models import TamirFotografi, FaturaKalemi, Randevu
from django.db.models import Prefetch

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"
    
    def dispatch(self, request, *args, **kwargs):
    
        if hasattr(request.user, 'profile') and request.user.profile.user_type == 'musteri':
            messages.warning(request, 'Bu sayfaya erişim izniniz bulunmamaktadır.')
            return redirect('musteri_portal')
        return super().dispatch(request, *args, **kwargs)
    
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
    son_is_emirleri = IsEmri.objects.all().order_by('-baslama_tarihi')[:5]
    
    return render(request, 'core/home.html', {
        'musteri_sayisi': musteri_sayisi,
        'arac_sayisi': arac_sayisi,
        'isemri_sayisi': isemri_sayisi,
        'son_is_emirleri': son_is_emirleri
    })



@login_required
def musteri_portal(request):
    # Kullanıcıya ait araçları bul
    araclar = Arac.objects.filter(musteri__user=request.user)
    
    # Araçlara ait aktif ve tamamlanmış iş emirlerini bul
    aktif_isemirler = IsEmri.objects.filter(
        arac__in=araclar,
        durum__in=['beklemede', 'incelemede', 'onarim_sureci', 'test_asamasi']
    ).order_by('-olusturma_tarihi')
    
    tamamlanan_isemirler = IsEmri.objects.filter(
        arac__in=araclar,
        durum='tamamlandi'
    ).order_by('-bitis_tarihi')
    
    context = {
        'aktif_isemirler': aktif_isemirler,
        'tamamlanan_isemirler': tamamlanan_isemirler,
        'araclar': araclar,
    }
    
    return render(request, 'core/musteri_portal.html', context)


@login_required
def tamir_durum(request, pk):
    is_emri = get_object_or_404(IsEmri, pk=pk)
    
    if hasattr(request.user, 'profile') and request.user.profile.user_type == 'musteri':
        try:
            musteri = Musteri.objects.get(user=request.user)
            if is_emri.arac.musteri != musteri:
                messages.error(request, 'Bu iş emrine erişim izniniz bulunmamaktadır.')
                return redirect('musteri_portal')
        except Musteri.DoesNotExist:
            messages.error(request, 'Müşteri bilgileriniz bulunamadı.')
            return redirect('musteri_portal')
    

    
    context = {
        'is_emri': is_emri,
    }
    
    return render(request, 'core/tamir_durum.html', context)



def musteri_list(request):
    musteriler = Musteri.objects.all()
    return render(request, "core/musteri_list.html", {"musteriler": musteriler})


@login_required
def arac_list(request):
    # Tüm araçları al
    araclar = Arac.objects.all().select_related('musteri')
    
    # IsEmri sorgusunu her araç için yapın
    for arac in araclar:
        # Alt çizgi ile başlayan isim kullanmayın!
        arac.son_islem = arac.get_son_isemri() if hasattr(arac, 'get_son_isemri') else None
    
    return render(request, 'core/arac_list.html', {'araclar': araclar})


@login_required
def isemri_list(request):
    # Sadece tamirci tipindeki kullanıcılar erişebilir
    if request.user.profile.user_type != 'tamirci':
        messages.error(request, 'Bu sayfaya erişim izniniz bulunmamaktadır.')
        return redirect('home')
    
    # Durum filtreleme
    durum = request.GET.get('durum')
    
    # İş emirlerini al
    if durum:
        isemirleri = IsEmri.objects.filter(durum=durum).order_by('-oncelik', '-olusturma_tarihi')
    else:
        isemirleri = IsEmri.objects.all().order_by('-oncelik', '-olusturma_tarihi')
    
    return render(request, 'core/isemri_list.html', {
        'isemirleri': isemirleri,
        'durum': durum
    })



from .forms import MusteriForm, AracForm

from django.shortcuts import render, redirect
from .forms import MusteriForm
from .models import Musteri, Arac, IsEmri, IsEmriIslem



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

            if form.cleaned_data.get('sorun_aciklama'):
                IsEmri.objects.create(
                    arac=arac,
                    aciklama=form.cleaned_data['sorun_aciklama'],
                    durum="beklemede"
                )
            else:
                IsEmri.objects.create(
                    arac=arac,
                    aciklama=f"{form.cleaned_data['marka']} {form.cleaned_data['model']} aracı için yeni kayıt",
                    durum="beklemede"
                )

            messages.success(request, f"{musteri.ad} müşterisi ve {arac.marka} {arac.model} aracı başarıyla eklendi.")
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
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            
            # UserProfile oluşturma işlemi
            user_type = form.cleaned_data.get('user_type')
            
            # Eğer profil otomatik oluşmadıysa oluştur
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(
                    user=user,
                    user_type=user_type
                )
            else:
                # Eğer profil otomatik oluştuysa sadece tipini güncelle
                user.profile.user_type = user_type
                user.profile.save()
            
            # Eğer müşteri tipinde kayıt olunduysa, Musteri modelinde de kayıt oluştur
            if user_type == 'musteri':
                # Telefon ve adres alanları için varsayılan değerler
                telefon = "Belirtilmedi"
                adres = "Belirtilmedi"
                
                # Kullanıcı adından bir isim oluştur (daha iyi bir yöntem eklenebilir)
                ad = user.first_name + ' ' + user.last_name if (user.first_name and user.last_name) else user.username
                
                # Aynı kullanıcı ile ilişkili müşteri kaydı var mı kontrol et
                musteri, created = Musteri.objects.get_or_create(
                    user=user,
                    defaults={
                        'ad': ad,
                        'telefon': telefon,
                        'adres': adres,
                        'email': user.email
                    }
                )
                
                if created:
                    messages.success(request, 'Hesabınız ve müşteri profiliniz başarıyla oluşturuldu!')
                else:
                    messages.info(request, 'Hesabınız oluşturuldu, mevcut müşteri profiliniz kullanılacak.')
            else:
                messages.success(request, 'Hesabınız başarıyla oluşturuldu!')
                
            login(request, user)
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


@login_required
def arac_ekle(request):
    """Araç ekleme görünümü"""
    if request.method == 'POST':
        form = AracForm(request.POST)
        if form.is_valid():
            arac = form.save(commit=False)
            if request.user.profile.user_type == 'musteri':
                try:
                    musteri = Musteri.objects.get(user=request.user)
                    arac.musteri = musteri
                except Musteri.DoesNotExist:
                    messages.error(request, "Müşteri kaydınız bulunamadı.")
                    return redirect('musteri_portal')
            arac.save()
            messages.success(request, "Araç başarıyla eklendi.")
            if request.user.profile.user_type == 'musteri':
                return redirect('musteri_arac_list')
            else:
                return redirect('arac_list')
    else:
        form = AracForm()
        if request.user.profile.user_type == 'musteri':
            form.fields.pop('musteri', None)
    
    return render(request, 'core/arac_ekle.html', {'form': form})



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

@login_required
def arac_detay(request, pk):
    arac = get_object_or_404(Arac, pk=pk)
    
    if hasattr(request.user, 'profile') and request.user.profile.user_type == 'musteri':
        try:
            musteri = Musteri.objects.get(user=request.user)
            if arac.musteri != musteri:
                messages.error(request, 'Bu araca erişim izniniz bulunmamaktadır.')
                return redirect('musteri_portal')
        except Musteri.DoesNotExist:
            messages.error(request, 'Müşteri bilgileriniz bulunamadı.')
            return redirect('musteri_portal')
    
    isemri_listesi = IsEmri.objects.filter(arac=arac).order_by('-baslama_tarihi')
    context = {
        'arac': arac,
        'isemri_listesi': isemri_listesi,
        'is_musteri': hasattr(request.user, 'profile') and request.user.profile.user_type == 'musteri'
    }
    return render(request, 'core/arac_detay.html', context)

def musteri_detay(request, pk):
    musteri = get_object_or_404(Musteri, id=pk)
    
    # İlişki adını doğru şekilde kullan
    araclar = Arac.objects.filter(musteri=musteri).prefetch_related('isemirleri')
    
    if request.method == 'POST':
        form = AracForm(request.POST)
        if form.is_valid():
            arac = form.save(commit=False)
            arac.musteri = musteri
            arac.save()
            messages.success(request, 'Araç başarıyla eklendi.')
            return redirect('musteri_detay', pk=musteri.id)
    else:
        form = AracForm(initial={'musteri': musteri})
    
    return render(request, 'core/musteri_detay.html', {
        'musteri': musteri,
        'araclar': araclar,
        'form': form
    })

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
    if request.method == 'POST':
        form = AracForm(request.POST)
        if form.is_valid():
            arac = form.save(commit=False)
            try:
                # Doğru yaklaşım: User'dan Musteri nesnesine erişim
                musteri = Musteri.objects.get(user=request.user)
                arac.musteri = musteri
            except Musteri.DoesNotExist:
                messages.error(request, "Müşteri kaydınız bulunamadı.")
                return redirect('musteri_portal')
            
            arac.save()
            messages.success(request, 'Aracınız başarıyla eklendi.')
            return redirect('musteri_arac_list')
    else:
        form = AracForm()
        # Müşteri alanını formdan kaldır
        form.fields.pop('musteri', None)
    
    return render(request, 'core/musteri_arac_form.html', {'form': form})

@login_required
def musteri_arac_list(request):
    """Müşteri araçları listesi görünümü"""
    try:
        musteri = Musteri.objects.get(user=request.user)
        araclar = Arac.objects.filter(musteri=musteri)
        return render(request, 'core/musteri_arac_list.html', {'araclar': araclar})
    except Musteri.DoesNotExist:
        messages.warning(request, "Müşteri kaydınız bulunamadı.")
        return redirect('musteri_portal')

@login_required
def musteri_isemri_list(request):
    # Sadece müşteri tipindeki kullanıcılar erişebilir
    if request.user.profile.user_type != 'musteri':
        messages.error(request, 'Bu sayfaya erişim izniniz bulunmamaktadır.')
        return redirect('home')
    
    try:
        musteri = Musteri.objects.get(user=request.user)
        isemirleri = IsEmri.objects.filter(arac__musteri=musteri).order_by('-baslama_tarihi')
    except Musteri.DoesNotExist:
        messages.error(request, 'Müşteri kaydınız bulunamadı.')
        return redirect('musteri_portal')
    
    return render(request, 'core/musteri_isemri_list.html', {
        'isemirleri': isemirleri
    })

@login_required
def musteri_isemri_ekle(request):
    if request.user.profile.user_type != 'musteri':
        messages.error(request, 'Bu sayfaya erişim izniniz bulunmamaktadır.')
        return redirect('home')
    
    try:
        musteri = Musteri.objects.get(user=request.user)
        araclar = Arac.objects.filter(musteri=musteri)
    except Musteri.DoesNotExist:
        messages.error(request, 'Müşteri kaydınız bulunamadı.')
        return redirect('musteri_portal')
    
    if not araclar.exists():
        messages.warning(request, 'İş emri oluşturmak için önce bir araç eklemelisiniz.')
        return redirect('musteri_arac_ekle')
    
    if request.method == 'POST':
        try:
            arac_id = request.POST.get('arac')
            aciklama = request.POST.get('aciklama')
            oncelik = request.POST.get('oncelik', 'normal')
            
            
            arac = Arac.objects.get(id=arac_id, musteri=musteri)
            
            
            isemri = IsEmri.objects.create(
                arac=arac,
                aciklama=aciklama,
                durum='beklemede',
                baslama_tarihi=timezone.now()
            )
            
            messages.success(request, f'#{isemri.id} numaralı iş emriniz başarıyla oluşturuldu.')
            return redirect('musteri_isemri_list')
            
        except Arac.DoesNotExist:
            messages.error(request, 'Geçersiz araç seçimi.')
        except Exception as e:
            messages.error(request, f'İş emri oluşturulurken bir hata oluştu: {str(e)}')
    
    return render(request, 'core/musteri_isemri_form.html', {
        'araclar': araclar
    })

@login_required
def musteri_isemri_iptal(request, isemri_id):
    if request.user.profile.user_type != 'musteri':
        messages.error(request, 'Bu sayfaya erişim izniniz bulunmamaktadır.')
        return redirect('home')
    
    try:
        musteri = Musteri.objects.get(user=request.user)
        isemri = IsEmri.objects.get(id=isemri_id, arac__musteri=musteri)
        
        if isemri.durum != 'beklemede':
            messages.error(request, 'Sadece beklemede olan iş emirleri iptal edilebilir.')
            return redirect('musteri_isemri_detay', isemri_id=isemri_id)
        
        if request.method == 'POST':
            isemri.durum = 'iptal'
            isemri.save()
            
            messages.success(request, f'#{isemri.id} numaralı iş emri başarıyla iptal edildi.')
            return redirect('musteri_isemri_list')
        
    except Musteri.DoesNotExist:
        messages.error(request, 'Müşteri kaydınız bulunamadı.')
        return redirect('musteri_portal')
    except IsEmri.DoesNotExist:
        messages.error(request, 'İş emri bulunamadı veya bu iş emrine erişim izniniz yok.')
        return redirect('musteri_isemri_list')
    
    return redirect('musteri_isemri_detay', isemri_id=isemri_id)

@login_required
def musteri_isemri_detay(request, isemri_id):
    # İş emrini bul ve kullanıcının erişim yetkisi olup olmadığını kontrol et
    isemri = get_object_or_404(IsEmri, pk=isemri_id)
    
    # Kullanıcının bu iş emrine erişim yetkisi var mı kontrol et
    if isemri.arac.musteri.user != request.user:
        messages.error(request, "Bu iş emrine erişim yetkiniz yok.")
        return redirect('musteri_portal')
    
    context = {
        'isemri': isemri,
    }
    
    return render(request, 'core/musteri_isemri_detay.html', context)

@login_required
def isemri_detay(request, isemri_id):
    # Sadece tamirci tipindeki kullanıcılar erişebilir
    if request.user.profile.user_type != 'tamirci':
        messages.error(request, 'Bu sayfaya erişim izniniz bulunmamaktadır.')
        return redirect('home')
    
    try:
        isemri = IsEmri.objects.get(id=isemri_id)
        islemler = IsEmriIslem.objects.filter(isemri=isemri).order_by('tarih')
        
    except IsEmri.DoesNotExist:
        messages.error(request, 'İş emri bulunamadı.')
        return redirect('isemri_list')
    
    return render(request, 'core/isemri_detay.html', {
        'isemri': isemri,
        'islemler': islemler
    })

def iletisim(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        messages.success(request, 'Mesajınız başarıyla gönderildi. En kısa sürede size dönüş yapacağız.')
        return redirect('iletisim')
    
    return render(request, 'core/iletisim.html')

@login_required
def musteri_fatura_goruntule(request, isemri_id):
    # İş emrini bul ve kullanıcının erişim yetkisi olup olmadığını kontrol et
    isemri = get_object_or_404(IsEmri, pk=isemri_id, durum='tamamlandi')
    
    # Kullanıcının bu iş emrine erişim yetkisi var mı kontrol et
    if isemri.arac.musteri.user != request.user:
        messages.error(request, "Bu faturaya erişim yetkiniz yok.")
        return redirect('musteri_portal')
    
    context = {
        'isemri': isemri,
    }
    
    return render(request, 'core/musteri_fatura_goruntule.html', context)

@login_required
def musteri_fatura_indir(request, isemri_id):
    # İş emrini bul ve kullanıcının erişim yetkisi olup olmadığını kontrol et
    isemri = get_object_or_404(IsEmri, pk=isemri_id, durum='tamamlandi')
    
    # Kullanıcının bu iş emrine erişim yetkisi var mı kontrol et
    if isemri.arac.musteri.user != request.user:
        messages.error(request, "Bu faturaya erişim yetkiniz yok.")
        return redirect('musteri_portal')
    
    # PDF oluştur
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Başlık
    p.setFont("Helvetica-Bold", 18)
    p.drawString(2*cm, height - 2*cm, f"FATURA #{isemri.id}")
    
    # Şirket bilgileri
    p.setFont("Helvetica", 10)
    p.drawString(2*cm, height - 3*cm, "Tamir Takip Sistemi")
    p.drawString(2*cm, height - 3.4*cm, "Örnek Cad. No:123")
    p.drawString(2*cm, height - 3.8*cm, "34000 İstanbul / Türkiye")
    p.drawString(2*cm, height - 4.2*cm, "Tel: +90 212 555 55 55")
    
    # Fatura bilgileri
    p.drawString(14*cm, height - 3*cm, f"Tarih: {isemri.tamamlanma_tarihi.strftime('%d.%m.%Y')}")
    p.drawString(14*cm, height - 3.4*cm, f"Fatura No: {isemri.id}")
    p.drawString(14*cm, height - 3.8*cm, f"İş Emri No: {isemri.id}")
    
    # Müşteri Bilgileri
    p.setFont("Helvetica-Bold", 12)
    p.drawString(2*cm, height - 5.5*cm, "Müşteri Bilgileri:")
    p.setFont("Helvetica", 10)
    p.drawString(2*cm, height - 6*cm, f"Ad Soyad: {isemri.arac.musteri.ad}")
    p.drawString(2*cm, height - 6.4*cm, f"Telefon: {isemri.arac.musteri.telefon}")
    
    # Araç Bilgileri
    p.setFont("Helvetica-Bold", 12)
    p.drawString(10*cm, height - 5.5*cm, "Araç Bilgileri:")
    p.setFont("Helvetica", 10)
    p.drawString(10*cm, height - 6*cm, f"Plaka: {isemri.arac.plaka}")
    p.drawString(10*cm, height - 6.4*cm, f"Marka/Model: {isemri.arac.marka} {isemri.arac.model}")
    
    # Fatura kalemleri tablosu
    data = [["#", "Hizmet/Parça", "Açıklama", "Miktar", "Birim Fiyat", "Toplam"]]
    
    for idx, kalem in enumerate(isemri.kalemler.all(), 1):
        data.append([
            str(idx),
            kalem.get_kalem_tipi_display(),
            kalem.aciklama,
            str(kalem.miktar),
            f"{kalem.birim_fiyat} ₺",
            f"{kalem.toplam_fiyat} ₺"
        ])
    
    # Toplam satırları
    data.append(["", "", "", "", "Ara Toplam:", f"{isemri.ara_toplam} ₺"])
    data.append(["", "", "", "", "KDV (%18):", f"{isemri.kdv_tutari} ₺"])
    data.append(["", "", "", "", "Genel Toplam:", f"{isemri.toplam_tutar} ₺"])
    
    # Tabloyu çiz
    table = Table(data, colWidths=[1*cm, 3*cm, 6*cm, 2*cm, 2.5*cm, 2.5*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -4), colors.white),
        ('BACKGROUND', (0, -3), (-1, -1), colors.lightgrey),
        ('FONTNAME', (4, -3), (5, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (3, 1), (5, -1), 'RIGHT'),
    ]))
    
    table.wrapOn(p, width, height)
    table.drawOn(p, 1.5*cm, height - 15*cm)
    
    # Not
    p.setFont("Helvetica-Bold", 10)
    p.drawString(2*cm, height - 18*cm, "Notlar:")
    p.setFont("Helvetica", 8)
    p.drawString(2*cm, height - 18.5*cm, "1. Tüm tamir işlemleri 3 ay garantilidir.")
    p.drawString(2*cm, height - 19*cm, "2. Yedek parçalar üretici garantisi kapsamındadır.")
    p.drawString(2*cm, height - 19.5*cm, "3. Ödeme fatura tarihinden itibaren 7 gün içinde yapılmalıdır.")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="fatura_{isemri.id}.pdf"'
    
    return response

@login_required
def musteri_randevu_olustur(request):
    
    araclar = Arac.objects.filter(musteri__user=request.user)
    
    if not araclar.exists():
        messages.warning(request, "Randevu oluşturmak için önce bir araç eklemelisiniz.")
        return redirect('arac_ekle')
    
    if request.method == 'POST':
        form = RandevuForm(request.POST, user=request.user)
        if form.is_valid():
            randevu = form.save(commit=False)
            randevu.musteri = request.user
            randevu.save()
            
            messages.success(request, "Randevunuz başarıyla oluşturuldu. En kısa sürede onaylanacaktır.")
            return redirect('musteri_portal')
    else:
        form = RandevuForm(user=request.user)
    
    return render(request, 'core/musteri_randevu_olustur.html', {'form': form})

@login_required
def musteri_araclar(request):
    # Kullanıcıya ait araçları al
    araclar = Arac.objects.filter(musteri__user=request.user).select_related('musteri').prefetch_related(
        Prefetch('isemirleri', queryset=IsEmri.objects.order_by('-olusturma_tarihi'), to_attr='son_isemriler')
    )
    
    # Her araca son iş emrini ekle
    for arac in araclar:
        if hasattr(arac, 'son_isemriler') and arac.son_isemriler:
            arac.son_isemri = arac.son_isemriler[0]
        else:
            arac.son_isemri = None
    
    return render(request, 'core/musteri_araclar.html', {'araclar': araclar})

@login_required
def arac_list(request):
    # Tüm araçları al (ama prefetch yapmadan)
    araclar = Arac.objects.all().select_related('musteri')
    
    # Her aracın son iş emrini bul
    for arac in araclar:
        # IsEmri modelinde arac alanı için related_name ne ise onu kullanın
        # Örnek: isemirleri, is_emirleri, tamir_talepleri vb.
        try:
            arac.son_isemri = IsEmri.objects.filter(arac=arac).order_by('-olusturma_tarihi').first()
        except:
            arac.son_isemri = None
    
    return render(request, 'core/arac_list.html', {'araclar': araclar})

@login_required
def isemri_olustur(request):
    """Yeni iş emri oluşturma fonksiyonu"""
    if request.method == 'POST':
        form = IsEmriForm(request.POST)
        if form.is_valid():
            isemri = form.save(commit=False)
            isemri.save()
            messages.success(request, 'İş emri başarıyla oluşturuldu.')
            return redirect('isemri_detay', isemri_id=isemri.id)
    else:
        initial = {}
        
        arac_id = request.GET.get('arac')
        if arac_id:
            try:
                arac = Arac.objects.get(id=arac_id)
                initial['arac'] = arac
            except Arac.DoesNotExist:
                pass
        
        form = IsEmriForm(initial=initial)
    
    return render(request, 'core/isemri_form.html', {
        'form': form,
        'is_new': True,
        'title': 'Yeni İş Emri Oluştur'
    })

@login_required
def arac_servis_gecmisi(request, arac_id):
    """Araç servis geçmişini görüntüle"""
    arac = get_object_or_404(Arac, id=arac_id)
    
    
    try:
        # İş emirlerini alın
        if hasattr(arac, 'isemirleri'):
            isemirleri = arac.isemirleri.all().order_by('-olusturma_tarihi')
        elif hasattr(arac, 'isemri_set'):
            isemirleri = arac.isemri_set.all().order_by('-olusturma_tarihi')
        else:
            
            isemirleri = IsEmri.objects.filter(arac=arac).order_by('-olusturma_tarihi')
    except Exception as e:
        print(f"Hata: {e}")
        isemirleri = []
    
    return render(request, 'core/arac_servis_gecmisi.html', {
        'arac': arac,
        'isemirleri': isemirleri
    })




