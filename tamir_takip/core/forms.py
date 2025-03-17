from django import forms
from .models import Musteri, Arac, IsEmri, UserProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
        fields = ['arac', 'aciklama', 'durum', 'teknisyen', 'yapilan_islemler', 
                 'kullanilan_parcalar', 'toplam_maliyet', 'kilometre', 'notlar', 
                 'baslama_tarihi', 'bitis_tarihi']
        widgets = {
            'baslama_tarihi': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'bitis_tarihi': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'aciklama': forms.Textarea(attrs={'rows': 3}),
            'yapilan_islemler': forms.Textarea(attrs={'rows': 3}),
            'kullanilan_parcalar': forms.Textarea(attrs={'rows': 3}),
            'notlar': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Kaydet"))