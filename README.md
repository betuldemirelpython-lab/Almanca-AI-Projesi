# Yapay Zeka Destekli Almanca Öğrenme Projesi

**Geliştirici:** Betül Altınkaynak Demirel  
**Lisans:** MIT  
**AI Modelleri:** Google Gemini 2.5 Flash / Groq LLaMA 3.3 (70B)  
**Dağıtım Platformu:** Vercel & FastAPI  

---

## 🌟 Proje Hakkında

**Yapay Zeka Destekli Almanca Öğrenme Projesi**, Türk kullanıcılar için Almanca öğrenim sürecini yapay zeka teknolojileriyle kişiselleştiren, derinleştiren ve hızlandıran modern bir dil platformudur.

Proje; Streamlit yerine Vercel uyumlu ultra modern glassmorphism web arayüzü ve FastAPI mikroservis mimarisi ile geliştirilmiştir.

---

## ✨ Temel Özellikler

### 1. 🎓 Almanca Seviyeleri ve Konu Kataloğu (A1 - C2)
- **A1, A2, B1, B2, C1, C2** seviyelerine ayrılmış geniş müfredat kataloğu.
- Her seviye için Gramer, Kelime Bilgisi, Günlük Konuşma, İş Almancası ve Akademik Dil kategorileri.
- Konulara tek tıkla tıklayarak anında derin yapay zeka analizine ulaşma.

### 2. ⚡ Gelişmiş Fiil Çekim Matrisi (6 Zaman x 6 Şahıs Zamiri)
- Girilen herhangi bir Almanca fiili (**gehen, machen, sprechen, sein, haben** vb.) 6 zaman diliminde tam çekimler:
  1. **Präsens** (Şimdiki / Geniş Zaman)
  2. **Präteritum** (Di'li Geçmiş Zaman)
  3. **Perfekt** (Geçmiş Zaman)
  4. **Plusquamperfekt** (-mişti'li Geçmiş)
  5. **Futur I** (Gelecek Zaman)
  6. **Futur II** (Gelecekte Tamamlanmış Zaman)
- 6 Şahıs Zamiri (*ich, du, er/sie/es, wir, ihr, sie/Sie*) matrisi.
- Yardımcı fiil (*haben* / *sein*) ve düzenli/düzensiz fiil tespiti.
- **Sesli Okunuş (Text-to-Speech)** desteği ile Almanca telaffuz dinleme.

### 3. 📖 Almanca ↔ Türkçe Akıllı Sözlük ve Çevirici
- İki yönlü canlı çeviri ve dilbilgisi kartı.
- Artikeller (**der, die, das**) için özel renk kodlamaları (Mavi, Pembe, Yeşil).
- İsim çoğul halleri (*Pluralformen*), okunuş rehberi ve örnek cümleler.

### 4. 🧠 AI Konu Özetleme ve Derin Analiz
- Kullanıcı tarafından girilen herhangi bir konunun detaylı açıklaması.
- Ana gramer kuralları, sık yapılan hatalar ve doğruları, pekiştirme soruları.

### 5. 📄 PDF Rapor İndirme (Export)
- Konu analizlerini, fiil tablolarını ve çalışma notlarını tek tıkla profesyonel tasarımlı PDF rapor dosyası olarak indirme.

### 6. 📁 Belge Analizi (PDF / DOCX Upload)
- Yüklenen PDF veya DOCX formatındaki Almanca çalışma metinlerini okuyarak yapay zeka ile seviye analizi ve kelime çıkarma.

---

## 🛠️ Teknoloji Stack

| Katman | Teknoloji |
|---|---|
| **Frontend** | Vercel Uyumlu Glassmorphic HTML5 / CSS3 / Vanilla JS |
| **Backend** | Python FastAPI |
| **AI Servisi** | Google Gemini 2.5 Flash / Groq LLaMA 3.3 (70B) |
| **Veritabanı** | SQLite + SQLAlchemy ORM |
| **Doğrulama** | Pydantic v2 |
| **PDF & Belge** | ReportLab, PyMuPDF (fitz), python-docx |
| **Environment** | python-dotenv |

---

## 📁 Proje Yapısı

```
Almanca-AI-Projesi/
│
├── index.html              # Vercel Uyumlu Frontend Web Arayüzü
├── api.py                  # FastAPI Backend API Servisleri
├── ai_service.py           # Gemini 2.5 Flash / Groq LLaMA 3.3 Entegrasyonu
├── database.py             # SQLite + SQLAlchemy Veritabanı Modülü
├── models.py               # Pydantic v2 Veri Modelleri
├── contract_service.py     # PDF Export & DOCX İşleme Servisi
├── prompts.py              # AI System Promptları ve A1-C2 Konu Kataloğu
├── requirements.txt        # Python Bağımlılıkları
├── vercel.json             # Vercel Dağıtım Konfigürasyonu
├── .env.example            # Örnek Environment Yapılandırması
├── .env                    # API Anahtarları (Gizli Tutun!)
├── .gitignore              # Git Engelleme Dosyası
│
├── uploads/                # Yüklenen Belgeler (Otomatik Oluşur)
├── data/                   # SQLite Veritabanı (Otomatik Oluşur)
│
└── README.md               # Dokümantasyon
```

---

## 🚀 Kurulum ve Yerel Çalıştırma

### 1. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 2. Environment (.env) Dosyasını Ayarlayın
`.env` dosyasını açıp API anahtarlarınızı tanımlayın:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
DEFAULT_AI_PROVIDER=gemini
```

### 3. FastAPI Sunucusunu Başlatın
```bash
uvicorn api:app --reload --port 8000
```

Tarayıcınızda `http://localhost:8000` adresini açarak uygulamayı kullanmaya başlayabilirsiniz!

---

## 🌐 Vercel Üzerinde Canlıya Alma (Deployment)

1. Projeyi GitHub reponuza push edin:
```bash
git init
git add .
git commit -m "Initial commit - Almanca AI Projesi"
git push origin main
```
2. [Vercel Dashboard](https://vercel.com) üzerinden reponuzu içe aktarın (Import).
3. Environment Variables kısmına `GEMINI_API_KEY` ve `GROQ_API_KEY` değerlerinizi ekleyin.
4. **Deploy** butonuna basarak canlıya alın!

---

**Geliştirici:** Betül Altınkaynak Demirel  
*Yapay Zeka Destekli Almanca Öğrenme Projesi*
