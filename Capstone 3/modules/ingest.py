import os
import pandas as pd
from dotenv import load_dotenv

from langchain_community.document_loaders import DataFrameLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from dotenv import find_dotenv
load_dotenv(find_dotenv())

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

def ingest_data():
    print("Memulai proses Ingest Data Resume...")
    
    file_path = "data/Resume.csv" 
    
    if not os.path.exists(file_path):
        print(f"Error: File tidak ditemukan di lokasi: {file_path}")
        return

    print(f"Membaca file CSV dari {file_path}...")
    df = pd.read_csv(file_path)
    
    # Hapus kolom HTML yang berat dan tidak perlu
    if 'Resume_html' in df.columns:
        df = df.drop(columns=['Resume_html'])
    
    # Hapus baris yang resume-nya kosong
    total_awal = len(df)
    df = df.dropna(subset=['Resume_str'])
    print(f"Data Cleaning: {total_awal} -> {len(df)} baris (menghapus data kosong).")

    # Load ke LangChain Document
    loader = DataFrameLoader(df, page_content_column="Resume_str")
    raw_documents = loader.load()
    print(f"Berhasil memuat {len(raw_documents)} document.")

    print("Melakukan Chunking Data...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""],
        length_function=len,
    )

    chunks = text_splitter.split_documents(raw_documents)
    print(f"Data dipecah menjadi {len(chunks)} chunks.")
    
    if chunks:
        print(f"Contoh Metadata Chunk 1: {chunks[0].metadata}")

    print(f"Menghubungkan ke Qdrant Cloud ({COLLECTION_NAME})...")
    
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    
    try:
        QdrantVectorStore.from_documents(
            documents=chunks,
            embedding=embeddings,
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            collection_name=COLLECTION_NAME,
            force_recreate=True 
        )
        print("SUKSES! Dataset Resume berhasil masuk ke Qdrant.")
        
    except Exception as e:
        print(f"Terjadi kesalahan saat upload: {e}")

if __name__ == "__main__":
    ingest_data()