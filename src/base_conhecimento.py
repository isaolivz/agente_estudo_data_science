import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pandas as pd
from langchain_core.documents import Document

class BaseConhecimento:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="intfloat/multilingual-e5-small",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.vector_store = None
    
    def carregar_pdfs(self, pasta="./data"):
        documentos = []
        for arquivo in os.listdir(pasta):
            if arquivo.endswith('.pdf'):
                caminho = os.path.join(pasta, arquivo)
                try:
                    loader = PyPDFLoader(caminho)
                    docs = loader.load()
                    documentos.extend(docs)
                except Exception as e:
                    print(f"Erro ao carregar {arquivo}: {e}")
        return documentos
    
    def carregar_txt(self, pasta="./data"):
        documentos = []
        for arquivo in os.listdir(pasta):
            if arquivo.endswith('.txt'):
                caminho = os.path.join(pasta, arquivo)
                try:
                    with open(caminho, 'r', encoding='utf-8') as f:
                        texto = f.read()
                        documentos.append({
                            "page_content": texto,
                            "metadata": {"fonte": arquivo}
                        })
                except Exception as e:
                    print(f"Erro ao carregar {arquivo}: {e}")
        return documentos
    
    def carregar_csvs(self, pasta="./data"):
        documentos = []
        for arquivo in os.listdir(pasta):
            if arquivo.endswith('.csv'):
                caminho = os.path.join(pasta, arquivo)
                try:
                    df = pd.read_csv(caminho)
                    for idx, row in df.iterrows():
                        texto = " | ".join([f"{col}: {val}" for col, val in row.items()])
                        documentos.append({
                            "page_content": texto,
                            "metadata": {"fonte": arquivo, "linha": idx}
                        })
                except Exception as e:
                    print(f"Erro ao carregar {arquivo}: {e}")
        return documentos
    
    def criar_vectorstore(self):
        docs = self.carregar_pdfs() + self.carregar_txt() + self.carregar_csvs()
        
        if not docs:
            print("Nenhum documento encontrado na pasta data/")
            return None
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        
        chunks = []
        for doc in docs:
            if isinstance(doc, dict):
                doc_obj = Document(
                    page_content=doc["page_content"],
                    metadata=doc["metadata"]
                )
                chunks.extend(splitter.split_documents([doc_obj]))
            else:
                chunks.extend(splitter.split_documents([doc]))
        
        self.vector_store = Chroma.from_documents(
            chunks,
            self.embeddings,
            persist_directory="./chroma_db"
        )
        print(f"Base criada com {len(chunks)} pedacos")
        return self.vector_store