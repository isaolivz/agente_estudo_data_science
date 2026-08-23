<img width="2245" height="378" alt="Cópia de Sem nome (59 4 x 10 cm) (1)" src="https://github.com/user-attachments/assets/fe0d7f77-bcdd-4fa2-aaf8-fcffba3bf24a" />




## Agente Inteligente para Consulta de Documentos

### Descrição Geral

Este projeto consiste em um agente inteligente que utiliza técnicas de **Recuperação Aumentada por Geração (RAG)** para responder perguntas em linguagem natural sobre documentos técnicos. O agente é capaz de processar arquivos **PDF** e **CSV**, extrair informações relevantes e gerar respostas precisas com base no conteúdo dos documentos.

A solução foi desenvolvida como parte do **Challenge Alura Agente**, com foco em demonstrar habilidades em Inteligência Artificial e processamento de linguagem natural

---

## 1. Arquitetura da Solução

A arquitetura do sistema é composta por quatro camadas principais:

<img width="1000" height="250" alt="image" src="https://github.com/user-attachments/assets/5eaa960a-8c97-452b-9e16-b547cd94c053" />


### 2. Fluxo de Processamento

1. **Indexação de Documentos**: Os arquivos PDF e CSV são carregados, divididos em chunks e transformados em vetores (embeddings) utilizando o modelo `intfloat/multilingual-e5-small` do Hugging Face. Os vetores são armazenados no ChromaDB.

2. **Consulta do Usuário**: Quando o usuário faz uma pergunta, o texto é convertido em um vetor utilizando o mesmo modelo de embeddings.

3. **Busca Semântica**: O ChromaDB realiza uma busca por similaridade vetorial, recuperando os chunks mais relevantes para a pergunta.

4. **Geração de Resposta**: O contexto recuperado é enviado para a API da Cohere, que gera uma resposta precisa e contextualizada, citando as fontes utilizadas.

---

## 3. Tecnologias e Ferramentas

| Categoria | Tecnologia | Descrição |
|-----------|------------|-----------|
| **Linguagem** | Python 3.12 | Linguagem principal do projeto |
| **Interface** | Streamlit 1.28.0 | Framework para criação da interface web |
| **Orquestração** | LangChain | Framework para construção de aplicações LLM |
| **Banco Vetorial** | ChromaDB | Banco de dados vetorial para busca semântica |
| **Embeddings** | Hugging Face (multilingual-e5-small) | Modelo para geração de embeddings em português |
| **LLM** | Cohere API | Modelo de linguagem para geração de respostas |
| **Processamento de PDF** | PyPDF | Extração de texto de arquivos PDF |
| **Processamento de CSV** | Pandas | Manipulação de dados tabulares |

---

## 4. Instruções para Execução

### 1. Clonar o Repositório

git clone https://github.com/isaolivz/agente_estudo_data_science

cd agente_estudo_data_science

### 2. Criar e Ativar Ambiente Virtual

#### Windows
python -m venv venv
venv\Scripts\activate

#### Linux/Mac
python3 -m venv venv
source venv/bin/activate

###  3. Instalar Dependências

pip install -r requirements.txt

### 4. Configurar Chave da API
Crie um arquivo .env na raiz do projeto:

env
COHERE_API_KEY=sua_chave_aqui

Para obter uma chave da Cohere, acesse: https://dashboard.cohere.com/api-keys

### 5. Adicionar Documentos
Coloque seus PDFs e CSVs na pasta data/:

### 6. Executar a Aplicação

streamlit run src/app.py
A aplicação estará disponível em: http://localhost:8501

### 7. Exemplos de Perguntas
-- Sobre Ciência de Dados

"O que é Ciência de Dados?"	- Conceitos básicos da área

"Quais são os pilares da Ciência de Dados?" -	Estrutura fundamental

"Explique o processo CRISP-DM" -	Metodologia de projetos

"O que é Machine Learning?" -	Subcampo da IA

-- Sobre Ferramentas

"Quais bibliotecas Python são usadas?" - Pergunta	Contexto

"Para que serve o Pandas?"	- Manipulação de dados

"O que é o Scikit-learn?" -	Biblioteca de Machine Learning

-- Sobre Carreira

"Como começar em Ciência de Dados?"	- Guia para iniciantes

"Quais habilidades são necessárias?" -	Competências técnicas e comportamentais

"O que faz um Cientista de Dados?" -	Atribuições do profissional

### 8. Exemplos de Respostas
<img width="1596" height="815" alt="image" src="https://github.com/user-attachments/assets/0e8a98bc-51f8-4768-adb8-36b4890fcba3" />


<img width="1600" height="825" alt="image" src="https://github.com/user-attachments/assets/8619e7a2-cb04-40f6-a0eb-b1d07ea0c507" />

<img width="1600" height="821" alt="image" src="https://github.com/user-attachments/assets/1c9f4f3e-39bc-41bb-a7c4-cc988903437f" />

---

## Deploy

O projeto está disponível em produção no seguinte endereço:

🔗 https://agenteestudodatascience-5egumgdyuvxqh39j8amfzb.streamlit.app/

