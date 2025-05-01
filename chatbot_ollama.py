
import os  # İşletim sistemi işlemleri için
import streamlit as st  # Web arayüzü için Streamlit
import pdfplumber  # PDF metinlerini çıkartmak için
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Metni parçalara bölmek için
from langchain.vectorstores import FAISS  # FAISS: vektör veritabanı
from langchain.embeddings import HuggingFaceEmbeddings  # Embedding için hafif bir model
from langchain.llms import Ollama  # Ollama üzerinden yerel LLM çağırmak için
from langchain.chains.question_answering import load_qa_chain  # Soru-cevap zinciri
from langchain.docstore.document import Document  # Her PDF parçası için metadata taşıyan nesne
import shutil  # Dosya/klsör silme işlemleri için

# Başlık
st.title("MEV'S ISTQB-AI TESTER EXAM PREPARATION APP")

# Yan panel: PDF yükleme
with st.sidebar:
    st.header("1. PDF Dosyasını Yükle")  # Sidebar başlığı
    uploaded_file = st.file_uploader("Bir PDF seçin", type="pdf")  # PDF yükleme alanı
    temizle = st.button("🔁 Vektör verisini sıfırla")  # FAISS verisini silme butonu

# Vektör klasörü ismi
vector_folder = "vector_index"

# Eğer kullanıcı sıfırlamaya bastıysa: FAISS dosyalarını sil
if temizle and os.path.exists(vector_folder):
    shutil.rmtree(vector_folder)  # klasörü sil
    st.warning("Vektör verisi sıfırlandı. Lütfen PDF'i tekrar yükleyin.")

# Embedding modeli (HuggingFace üzerinden küçük boyutlu model)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Eğer FAISS verisi yoksa ve PDF yüklenmişse → veritabanını oluştur
if uploaded_file and not os.path.exists(vector_folder):
    with pdfplumber.open(uploaded_file) as pdf:
        documents = []
        for i, page in enumerate(pdf.pages):  # PDF’i sayfa sayfa gez
            text = page.extract_text()  # Metni çıkar
            if text:
                doc = Document(page_content=text, metadata={"page": i + 1})  # Sayfa metni ve numarası
                documents.append(doc)

    # Metni küçük parçalara böl
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,  # Her parçanın max uzunluğu
        chunk_overlap=150  # Parçalar arası örtüşme
    )
    chunks = text_splitter.split_documents(documents)  # Chunk'lara böl

    # FAISS vektör veritabanını oluştur ve diske kaydet
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(vector_folder)  # "vector_index" klasörüne kayıt
    st.success("✅ PDF vektör verisine dönüştürüldü ve kaydedildi.")

# Eğer FAISS verisi varsa → yükle
if os.path.exists(vector_folder):
    try:
        vector_store = FAISS.load_local(
            vector_folder,
            embeddings,
            allow_dangerous_deserialization=True  # Güvenli yükleme izni (sen oluşturduysan güvenli)
        )
    except Exception as e:
        st.error(f" FAISS dosyası yüklenirken hata oluştu: {e}")
        vector_store = None
else:
    vector_store = None

# Soru cevap bölümü aktifse (vektör verisi yüklüyse)
if vector_store:
    st.header("Let’s see if your question makes sense. 🧐")  # Soru kutusu başlığı
    user_question = st.text_input("")  # Soru giriş alanı

    if user_question:
        docs = vector_store.similarity_search(user_question, k=3)  # En alakalı 3 chunk'ı getir

        # LLM modelini çağır (Ollama - Mistral)
        llm = Ollama(model="mistral", temperature=0)  # Cevaplar sabit, rastgelelik yok
        chain = load_qa_chain(llm, chain_type="stuff")  # Basit Soru-Cevap zinciri
        answer = chain.run(input_documents=docs, question=user_question)  # Cevabı üret

        st.markdown("### 📢 Not bad for a robot, huh?")  # Cevap başlığı
        st.write(answer)  # Cevabı göster

        st.markdown("### Don’t believe me? Read these:")  # Kaynak başlığı
        for doc in docs:
            page = doc.metadata.get("page", "?")  # Sayfa numarası al
            snippet = doc.page_content[:200].replace("\n", " ")  # İlk 200 karakteri al, satır sonlarını sil
            st.markdown(f"- Page {page}: _{snippet}..._")  # Kaynak snippet'i göster
