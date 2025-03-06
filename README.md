  <a href="https://www.python.org" target="_blank" rel="noreferrer"> 
        <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> 
  </a> 
   
# Tamir Takip Sistemi

## Proje Açıklaması
Tamir Takip Sistemi, tamir işlemlerini izlemek ve yönetmek için geliştirilmiş bir uygulamadır. Bu sistem, müşteri ve araç bilgilerini kaydetme, iş emirlerini yönetme ve tamir durumlarını izleme gibi özellikler sunar.

## Özellikler
- Müşteri kayıtlarını ekleme, güncelleme ve silme
- Araç kayıtlarını ekleme, güncelleme ve silme
- İş emirlerini ekleme, güncelleme ve silme
- Tamir durumlarını izleme
- Kullanıcı yönetimi ve yetkilendirme
- API desteği ile dış sistemlerle entegrasyon

## Kurulum
Projenin çalıştırılabilmesi için aşağıdaki adımları izleyin:

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/arazumut/RepairTracking.git
cd RepairTracking
```

### 2. Sanal Ortam Oluşturun ve Aktif Edin
```bash
python -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate
```

### 3. Gerekli Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Veritabanı Migrations İşlemlerini Gerçekleştirin
```bash
python manage.py migrate
```

### 5. Yönetici Kullanıcı Oluşturun
```bash
python manage.py createsuperuser
```

### 6. Uygulamayı Başlatın
```bash
python manage.py runserver
```

### 7. Tarayıcıda Uygulamayı Açın
Tarayıcınızda [http://127.0.0.1:8000](http://127.0.0.1:8000) adresine giderek uygulamayı kullanmaya başlayabilirsiniz.

## Kullanım

### Yönetici Paneli
Yönetici paneline erişmek için [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) adresine gidin ve oluşturduğunuz yönetici hesabı ile giriş yapın.

### API Kullanımı
API uç noktalarına erişmek için [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/) adresini kullanabilirsiniz. Örnek uç noktalar:
- [http://127.0.0.1:8000/api/musteriler/](http://127.0.0.1:8000/api/musteriler/)
- [http://127.0.0.1:8000/api/araclar/](http://127.0.0.1:8000/api/araclar/)
- [http://127.0.0.1:8000/api/isemirleri/](http://127.0.0.1:8000/api/isemirleri/)

## Katkıda Bulunma
Katkıda bulunmak isterseniz, lütfen bir pull request gönderin veya bir issue açın.
