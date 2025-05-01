import os
import streamlit as st
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document
import shutil

# Başlık
st.title("MEV'S ISTQB-AI TESTER EXAM PREPARATION APP")

# Yan panel: PDF yükleme
with st.sidebar:
    st.header("1. PDF Dosyasını Yükle")
    uploaded_file = st.file_uploader("Bir PDF seçin", type="pdf")
    temizle = st.button("🔁 Vektör verisini sıfırla")

# Vektör klasörü ismi
vector_folder = "vector_index"

# Eğer kullanıcı temizlemek istediyse: klasörü sil
if temizle and os.path.exists(vector_folder):
    shutil.rmtree(vector_folder)
    st.warning("Vektör verisi sıfırlandı. Lütfen PDF'i tekrar yükleyin.")

# Embedding modeli
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Eğer FAISS dosyası yoksa ve PDF yüklendiyse → oluştur
if uploaded_file and not os.path.exists(vector_folder):
    with pdfplumber.open(uploaded_file) as pdf:
        documents = []
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                doc = Document(page_content=text, metadata={"page": i + 1})
                documents.append(doc)

    # Parçalara böl
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=150
    )
    chunks = text_splitter.split_documents(documents)

    # Vektör veritabanını oluştur ve kaydet
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(vector_folder)
    st.success("✅ PDF vektör verisine dönüştürüldü ve kaydedildi.")

# Eğer FAISS dosyası varsa → yükle
if os.path.exists(vector_folder):
    try:
        vector_store = FAISS.load_local(
            vector_folder,
            embeddings,
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        st.error(f" FAISS dosyası yüklenirken hata oluştu: {e}")
        vector_store = None
else:
    vector_store = None

# Soru cevap bölümü
if vector_store:
    st.header("Let’s see if your question makes sense. 🧐")
    user_question = st.text_input("")

    if user_question:
        # En alakalı parçaları bul
        docs = vector_store.similarity_search(user_question, k=3)

        # Ollama (mistral) modeliyle cevap oluştur
        llm = Ollama(model="mistral", temperature=0)
        chain = load_qa_chain(llm, chain_type="stuff")
        answer = chain.run(input_documents=docs, question=user_question)

        # Cevap göster
        st.markdown("### 📢 Not bad for a robot, huh?” ")
        st.write(answer)

        # Kaynakları göster
        st.markdown("### Don’t believe me? Read these:")
        for doc in docs:
            page = doc.metadata.get("page", "?")
            snippet = doc.page_content[:200].replace("\n", " ")
            st.markdown(f"- Page {page}: _{snippet}..._")