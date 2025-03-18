from django import forms
from .models import Musteri, Arac, IsEmri, UserProfile, Randevu
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(
        choices=UserProfile.USER_TYPES,
        required=True,
        label="Kullanıcı Tipi",
        widget=forms.RadioSelect
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            user.profile.user_type = self.cleaned_data['user_type']
            user.profile.save()
            
        return user


class MusteriForm(forms.ModelForm):
    email = forms.EmailField(required=False, label="E-posta")
    marka = forms.CharField(max_length=100, required=True, label="Araç Markası")
    model = forms.CharField(max_length=100, required=True, label="Araç Modeli")
    plaka = forms.CharField(max_length=20, required=True, label="Plaka")
    uretim_yili = forms.IntegerField(required=True, label="Üretim Yılı")
    sorun_aciklama = forms.CharField(widget=forms.Textarea, required=False, label="Araç Sorunu")

    class Meta:
        model = Musteri
        fields = ['ad', 'telefon', 'email', 'adres', 'marka', 'model', 'plaka', 'uretim_yili', 'sorun_aciklama']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Kaydet"))

class AracForm(forms.ModelForm):
    class Meta:
        model = Arac
        fields = ['musteri', 'marka', 'model', 'plaka', 'uretim_yili']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Kaydet"))

class IsEmriForm(forms.ModelForm):
    class Meta:
        model = IsEmri
        fields = ['arac', 'aciklama', 'durum', 'oncelik']
        widgets = {
            'arac': forms.Select(attrs={'class': 'form-select'}),
            'aciklama': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'durum': forms.Select(attrs={'class': 'form-select'}),
            'oncelik': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Kaydet"))

class RandevuForm(forms.ModelForm):
    class Meta:
        model = Randevu
        fields = ['arac', 'randevu_tarihi', 'randevu_saati', 'ariza_aciklamasi', 'randevu_tipi', 'iletisim_tercihi', 'onay']
        widgets = {
            'arac': forms.Select(attrs={'class': 'form-select'}),
            'randevu_tarihi': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'randevu_saati': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'ariza_aciklamasi': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'randevu_tipi': forms.Select(attrs={'class': 'form-select'}),
            'iletisim_tercihi': forms.Select(attrs={'class': 'form-select'}),
            'onay': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RandevuForm, self).__init__(*args, **kwargs)
        
        # Kullanıcıya ait araçları filtrele
        if user:
            self.fields['arac'].queryset = Arac.objects.filter(musteri__user=user)
    
    def clean_randevu_tarihi(self):
        randevu_tarihi = self.cleaned_data.get('randevu_tarihi')
        bugun = timezone.now().date()
        
        if randevu_tarihi < bugun + datetime.timedelta(days=1):
            raise forms.ValidationError('Randevu tarihi en az yarın olmalıdır.')
        
        # Hafta sonu kontrolü
        if randevu_tarihi.weekday() >= 5:  # 5=Cumartesi, 6=Pazar
            raise forms.ValidationError('Hafta sonu randevu alınamaz.')
        
        return randevu_tarihi
    
    def clean_randevu_saati(self):
        randevu_saati = self.cleaned_data.get('randevu_saati')
        
        # Çalışma saatleri kontrolü
        if randevu_saati.hour < 9 or randevu_saati.hour >= 18:
            raise forms.ValidationError('Randevu saati 09:00 - 18:00 arasında olmalıdır.')
        
        return randevu_saati