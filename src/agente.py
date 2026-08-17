import cohere
from dotenv import load_dotenv
import os
from base_conhecimento import BaseConhecimento

load_dotenv()

class AgenteInteligente:
    def __init__(self):
        self.base = BaseConhecimento()
        self.base.criar_vectorstore()
        
        if not self.base.vector_store:
            print("Base de conhecimento vazia")
            return
        
        self.co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))
    
    def perguntar(self, pergunta):
        if not self.base.vector_store:
            return "Base de conhecimento nao inicializada."
        
        docs = self.base.vector_store.similarity_search(pergunta, k=3)
        
        contexto = "\n\n".join([doc.page_content for doc in docs])
        
        prompt = f"""Voce e um assistente especializado em analisar documentos.
Use APENAS as informacoes do contexto abaixo para responder.

Contexto:
{contexto}

Pergunta: {pergunta}

Resposta:"""
        
        try:
            resposta = self.co.chat(
                model="command-r-plus-08-2024",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            texto = resposta.message.content[0].text
            
            fontes = []
            for doc in docs[:2]:
                fonte = doc.metadata.get("fonte", "Documento")
                pagina = doc.metadata.get("page", "N/A")
                fontes.append(f"{fonte} (pag. {pagina})")
            
            if fontes:
                texto += f"\n\nFonte: {', '.join(fontes)}"
            
            return texto
        
        except Exception as e:
            return f"Erro: {str(e)}"