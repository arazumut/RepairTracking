
document.addEventListener('DOMContentLoaded', function() {

    
    const photoGallery = document.querySelectorAll('.photo-gallery img');
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.getElementById('lightbox-caption');
    const lightboxClose = document.querySelector('.lightbox-close');

    if (photoGallery.length > 0 && lightbox) {
        photoGallery.forEach(img => {
            img.addEventListener('click', e => {
                lightboxImg.src = e.target.src;
                lightboxCaption.textContent = e.target.alt || 'Tamir fotoğrafı';
                lightbox.style.display = 'flex';
                document.body.style.overflow = 'hidden';
            });
        });

        lightboxClose.addEventListener('click', () => {
            lightbox.style.display = 'none';
            document.body.style.overflow = 'auto';
        });

        lightbox.addEventListener('click', e => {
            if (e.target === lightbox) {
                lightbox.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    }


    const randevuForm = document.querySelector('form.needs-validation');
    if (randevuForm) {
    
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        const minDate = tomorrow.toISOString().split('T')[0];
        
        const datePicker = document.getElementById('id_randevu_tarihi');
        if (datePicker) {
            datePicker.setAttribute('min', minDate);
            
        
            datePicker.addEventListener('input', function() {
                const selectedDate = new Date(this.value);
                const dayOfWeek = selectedDate.getDay();
                
                
                if (dayOfWeek === 0 || dayOfWeek === 6) {
                    this.setCustomValidity('Hafta sonu randevu alınamaz. Lütfen hafta içi bir tarih seçin.');
                } else {
                    this.setCustomValidity('');
                }
            });
        }
        

        const timePicker = document.getElementById('id_randevu_saati');
        if (timePicker) {
            timePicker.addEventListener('input', function() {
                const selectedTime = this.value;
                const hour = parseInt(selectedTime.split(':')[0]);
                
                if (hour < 9 || hour >= 18) {
                    this.setCustomValidity('Çalışma saatleri 09:00 - 18:00 arasındadır. Lütfen bu aralıkta bir saat seçin.');
                } else {
                    this.setCustomValidity('');
                }
            });
        }
    }

    
    const timelineItems = document.querySelectorAll('.timeline-item');
    if (timelineItems.length > 0) {
        timelineItems.forEach((item, index) => {
            setTimeout(() => {
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }, 100 * index);
        });
    }
}); 