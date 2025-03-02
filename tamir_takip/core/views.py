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


def musteri_ekle(request):
    if request.method == "POST":
        form = MusteriForm(request.POST)
        if form.is_valid():
            form.save()
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
            login(request, user)  # Kullanıcıyı otomatik giriş yap
            return redirect('home')  # Anasayfaya yönlendir
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})




