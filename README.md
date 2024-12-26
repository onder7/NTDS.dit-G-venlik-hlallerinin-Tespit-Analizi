# NTDS.dit-G-venlik-hlallerinin-Tespit-Analizi
Kullanıcı Arayüzü:

Başlangıç ve bitiş tarihi seçimi
Analiz başlatma, rapor oluşturma ve temizleme butonları
İki sekme: Olay günlükleri ve şüpheli dosyalar
Durum çubuğu


Olay Günlüğü Analizi:

ESENT provider'ından belirtilen event ID'leri (216, 325, 326, 327) için kayıtları çeker
Olayları kronolojik sırayla listeler
Şüpheli paternleri tespit eder (hızlı takma-çıkarma, yeni veritabanı oluşturma, konum değişiklikleri)


Dosya Analizi:

Masaüstündeki ZIP dosyalarını tarar
Boyut ve oluşturma zamanına göre şüpheli dosyaları tespit eder


Raporlama:

Tüm bulguları detaylı bir rapora dönüştürür
Raporu tarih damgalı bir dosyaya kaydeder



Kullanmak için:

Scripti çalıştırın
Analiz tarih aralığını seçin
"Analizi Başlat" butonuna tıklayın
Sonuçları inceleyin
Gerekirse rapor oluşturun

Not: Bu uygulamanın çalışması için:

Python 3.x
tkinter (genellikle Python ile gelir)
Windows işletim sistemi
PowerShell erişimi gereklidir

Şüpheli aktivite tespit edildiğinde daha detaylı adli analiz yapılması önerilir.
