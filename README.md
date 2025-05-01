#  MEV'S ISTQB AI TESTING EXAM PREP (Powered by Ollama)

Bu uygulama, ISTQB AI Tester sertifikasına hazırlık sürecinde yardımcı bir araç olarak geliştirilmiş; aynı zamanda dar yapay zekayı (Narrow AI) uygulamalı olarak anlamak için eğitim amaçlı kullanılmıştır.
Kullanıcılar, PDF formatındaki syllabus dosyasını yükleyerek içerikle ilgili sorular sorabilir ve sayfa numarasıyla birlikte yanıtlar alabilirler.

![ollamachatbot](https://github.com/user-attachments/assets/973a6d83-c5f0-4904-b1d9-330906fa623d)


---

##  Özellikler

-  PDF dosyalarından metin çıkarma
-  Metni küçük parçalara ayırarak anlamlı şekilde işleme
-  Ollama üzerindeki Mistral dil modeli ile soru-cevap yapma
-  FAISS kullanarak hızlı metin araması
-  Streamlit ile sade ve eğlenceli bir web arayüz
-  Sayfa numarası gösterimli kaynak listesi


---

## Gereksinimler

Aşağıdaki kütüphanelerin kurulu olduğundan emin olun:

```
pip install streamlit pdfplumber langchain faiss-cpu sentence-transformers
```

Ayrıca [Ollama](https://ollama.com) kurulmalı ve terminalde aşağıdaki komutla çalışıyor olmalı:

```
ollama run mistral
```

---

##  Kullanım

1. Projeyi klonlayın:
   ```
   git clone https://github.com/kullaniciadi/mev-ollama-ai-chatbot.git
   cd mev-ollama-ai-chatbot
   ```

2. Gerekli bağımlılıkları yükleyin:
   ```
   pip install -r requirements.txt
   ```

3. Uygulamayı başlatın:
   ```
   streamlit run chatbot_ollama.py
   ```

4. Tarayıcıda açılan arayüzde PDF yükleyin, sorunuzu yazın, cevabı ve kaynak sayfasını görün!

 Windows kullanıcıları için `app.bat` dosyası sayesinde terminale girmeden başlatılabilir.

---

##  Ekran Görüntüsü

![ollamachatbot](https://github.com/user-attachments/assets/cc8a9b17-47e9-452b-a3b8-f3078d221cd7)


---

## Geliştirme Süreci

Bu proje, **ISTQB AI Tester sınavına hazırlanırken**  
hem belge tabanlı Narrow AI uygulamalarını öğrenmek,  
hem de offline, ücretsiz bir chatbot geliştirmek amacıyla oluşturulmuştur.


---

##  Kullanılan Teknolojiler

- Python 3.10+
- Streamlit
- LangChain
- FAISS
- HuggingFace Embeddings (`all-MiniLM-L6-v2`)
- Ollama (Mistral modeli)

---

##  Örnek Soru

> **Soru:** What is machine learning?  
> **Cevap:** Model syllabus içinden en alakalı 3 sayfayı alır, özet bir cevap oluşturur ve kaynakları sayfa numarasıyla birlikte gösterir.

---

##  Hazırlayan

**Mevlüt Salman  
