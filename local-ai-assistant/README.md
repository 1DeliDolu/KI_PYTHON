# Multi-Task AI Assistant

Bu proje, çeşitli AI görevlerini gerçekleştirebilen çok işlevli bir asistan uygulamasıdır.

## Özellikler

- **Wikipedia Sorgusu**: Wikipedia'da arama yapma ve bilgi alma
- **Belge Okuyucu**: PDF, DOCX, TXT, RTF formatlarındaki belgeleri okuma ve analiz etme
- **Görsel Analizi**: Resimleri analiz etme, renk analizi, kenar tespiti, yüz tanıma
- **Video Analizi**: Video dosyalarını analiz etme, hareket tespiti, sahne değişimi
- **Çeviri**: Metinleri farklı diller arasında çevirme

## Kurulum

1. Repository'yi klonlayın:
```bash
git clone <repository-url>
cd local-ai-assistant
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Gerekli dizinleri oluşturun:
```bash
mkdir -p data models temp
```

## Kullanım

### Etkileşimli Mod
```bash
python main.py --interactive
```

### Komut Satırı Modu

**Wikipedia Sorgusu:**
```bash
python main.py --wikipedia "artificial intelligence"
```

**Belge Okuma:**
```bash
python main.py --document "path/to/document.pdf"
```

**Görsel Analizi:**
```bash
python main.py --image "path/to/image.jpg"
```

**Video Analizi:**
```bash
python main.py --video "path/to/video.mp4"
```

**Çeviri:**
```bash
python main.py --translate "Hello world" --target-lang tr
```

## Proje Yapısı

```
Multi-Task-AI-Assistant/
│
├── main.py                      # Ana uygulama giriş noktası
├── config.py                    # Konfigürasyon ayarları
├── requirements.txt             # Bağımlılık listesi
├── data/                        # Veri setleri için dizin
├── models/                      # Önceden eğitilmiş modeller
├── scripts/                     # Çeşitli işlevsellikler için scriptler
│   ├── wikipedia_query.py       # Wikipedia sorgu scripti
│   ├── document_reader.py       # Belge okuma scripti
│   ├── image_analysis.py        # Görsel analiz scripti
│   ├── video_analysis.py        # Video analiz scripti
│   └── translator.py            # Çeviri scripti
├── tests/                       # Birim testler
└── notebooks/                   # Deneyim için Jupyter notebook'lar
```

## Desteklenen Formatlar

### Belgeler
- PDF (.pdf)
- Microsoft Word (.docx, .doc)
- Plain Text (.txt)
- Rich Text Format (.rtf)

### Görseller
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tiff)

### Videolar
- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- WMV (.wmv)
- FLV (.flv)

## Desteklenen Diller (Çeviri)

- Türkçe (tr)
- İngilizce (en)
- Almanca (de)
- Fransızca (fr)
- İspanyolca (es)
- İtalyanca (it)
- Rusça (ru)
- Çince (zh)
- Japonca (ja)
- Korece (ko)
- Arapça (ar)
- Portekizce (pt)
- Hollandaca (nl)
- İsveççe (sv)
- Danca (da)
- Norveççe (no)
- Lehçe (pl)
- Çekçe (cs)
- Macarca (hu)
- Yunanca (el)
- İbranca (he)
- Hintçe (hi)
- Tayca (th)
- Vietnamca (vi)

## Konfigürasyon

Uygulama ayarları `config.py` dosyasında yapılandırılabilir:

- Dosya boyutu sınırları
- Desteklenen formatlar
- API anahtarları (çevre değişkenleri olarak)
- Model ayarları

## Çevre Değişkenleri

Aşağıdaki çevre değişkenlerini isteğe bağlı olarak ayarlayabilirsiniz:

```bash
export OPENAI_API_KEY="your-openai-api-key"
export AZURE_TRANSLATOR_KEY="your-azure-translator-key"
export AZURE_TRANSLATOR_REGION="your-azure-region"
```

## Geliştirme

### Test Çalıştırma
```bash
pytest tests/
```

### Yeni Özellik Ekleme
1. `scripts/` dizininde yeni modül oluşturun
2. `main.py` dosyasında modülü import edin
3. Gerekli menü seçeneklerini ekleyin
4. Test yazın

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'i push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## Sorun Giderme

### Yaygın Sorunlar

1. **ModuleNotFoundError**: Tüm bağımlılıkların yüklü olduğundan emin olun
2. **Dosya okuma hatası**: Dosya yollarının doğru olduğunu kontrol edin
3. **Çeviri hatası**: İnternet bağlantınızı kontrol edin

### Loglama

Debug modunu etkinleştirmek için `config.py` dosyasında `DEBUG = True` yapın.

## İletişim

Sorularınız için issue açabilirsiniz.