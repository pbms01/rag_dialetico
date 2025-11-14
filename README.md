# 🏛️ Sistema RAG - Geração Automática de Contestações Jurídicas

Sistema inteligente para geração automática de contestações jurídicas em ações de planos de saúde, utilizando **RAG (Retrieval-Augmented Generation)** com busca vetorial hierárquica e **Claude Sonnet 4.5**.

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Instalação](#instalação)
4. [Configuração](#configuração)
5. [Como Usar](#como-usar)
6. [Estrutura do Projeto](#estrutura-do-projeto)
7. [Metodologia RAG](#metodologia-rag)
8. [Custos](#custos)
9. [Desenvolvimento](#desenvolvimento)

---

## 🎯 Visão Geral

### **Objetivo**
Automatizar a geração de contestações jurídicas de alta qualidade para ações movidas contra operadoras de planos de saúde, reduzindo tempo de resposta e mantendo qualidade técnica profissional.

### **Funcionalidades Principais**
- ✅ Upload de petição inicial (PDF, DOCX, TXT)
- ✅ Análise estruturada automática da petição
- ✅ Classificação automática do tipo de caso
- ✅ Recuperação hierárquica de conhecimento jurídico (RAG 3 níveis)
- ✅ Geração de contestação com Claude Sonnet 4.5
- ✅ Validação automática de qualidade
- ✅ Export para DOCX formatado profissionalmente
- ✅ Interface web intuitiva (Streamlit)
- ✅ Controle de temperatura e top-k para ajuste fino

### **Tipos de Caso Suportados**
1. 🚫 **Aviso Prévio / Cancelamento** - Cancelamento sem aviso adequado
2. ⏰ **Demora na Autorização** - Demora excessiva em autorizações
3. 🏠 **Home Care** - Negativa de cobertura de atendimento domiciliar
4. 💰 **Reembolso** - Problemas com reembolso de despesas
5. 🎯 **Terapias / Livre Escolha** - Restrições em escolha de profissionais

---

## 🏗️ Arquitetura

### **Pipeline de Geração**

```
┌─────────────────┐
│  Petição Inicial│
│   (Upload)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Processamento  │ ──► Extração: autor, réu, fatos, pedidos
│   da Petição    │     Classificação: tipo de caso
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Retrieval RAG   │ ──► Nível 1: Contexto global (10 chunks)
│  (3 Níveis)     │     Nível 2: Seções processuais (20 chunks)
│                 │     Nível 3: Precedentes/artigos (15 chunks)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Context Builder │ ──► Síntese e organização do contexto
│                 │     Ranqueamento e deduplicação
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Claude API     │ ──► Geração da contestação
│  (Sonnet 4.5)   │     Temp: 0.3-0.9, Top-k: 20-60
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Validação     │ ──► Métricas de qualidade
│                 │     Alertas e verificações
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Formatação DOCX │ ──► Documento profissional
│                 │     Pronto para uso
└─────────────────┘
```

### **Componentes Técnicos**

| Componente | Tecnologia | Função |
|------------|-----------|--------|
| **Vector Store** | ChromaDB | Armazenamento e busca vetorial |
| **Embeddings** | multilingual-e5-large | Geração de embeddings (1024 dim) |
| **LLM** | Claude Sonnet 4.5 | Geração de texto jurídico |
| **Interface** | Streamlit | Web app interativa |
| **Processamento** | PyPDF2, python-docx | Extração de texto |

---

## 🚀 Instalação

### **Pré-requisitos**
- Python 3.10 ou superior
- 4GB+ RAM disponível
- GPU (opcional, acelera embeddings)
- Chave API Anthropic

### **Passos**

1. **Clone ou baixe o projeto**
```bash
cd c:\users\pbm_s\onedrive\rag pimenta
```

2. **Crie ambiente virtual**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Instale dependências**
```bash
pip install -r requirements.txt
```

4. **Configure variáveis de ambiente**
```bash
# Crie arquivo .env
copy .env.example .env

# Edite .env e adicione sua API key:
ANTHROPIC_API_KEY=sk-ant-...
```

---

## ⚙️ Configuração

### **Arquivo `.env`**
```bash
# API Keys
ANTHROPIC_API_KEY=sk-ant-api03-...

# Paths (ajustar se necessário)
VECTOR_STORE_DIR=c:\users\pbm_s\onedrive\rag pimenta\output_rag\vector_store
```

### **Configurações Avançadas**
Edite `config/settings.py` para ajustar:
- Parâmetros de retrieval (top-k por nível)
- Limites de tokens
- Parâmetros do Claude (temperatura, top-k)
- Tipos de caso e classificação

---

## 📖 Como Usar

### **1. Iniciar a Aplicação**

```bash
cd rag_contestacoes
streamlit run app.py
```

A interface abrirá em: `http://localhost:8501`

### **2. Upload da Petição**
1. Na aba **"Gerar Contestação"**, faça upload do arquivo (PDF/DOCX/TXT)
2. Aguarde processamento automático

### **3. Configurar Parâmetros**
- **Temperatura (0.3-0.9):**
  - 0.3-0.5: Mais conservadora, segue estritamente o contexto
  - 0.6-0.7: **Recomendado** - Balanceada
  - 0.8-0.9: Mais criativa (arriscado para jurídico)

- **Top-k (20-60):**
  - 20-30: Mais focada
  - 40-50: **Recomendado** - Balanceada
  - 50-60: Maior diversidade vocabular

### **4. Gerar Contestação**
1. Clique em **"🚀 GERAR CONTESTAÇÃO"**
2. Aguarde ~20-35 segundos
3. Visualize resultado e métricas de qualidade

### **5. Download**
- **📥 Download DOCX:** Documento formatado profissionalmente
- **📋 Copiar Texto:** Copiar para outro editor

### **6. Abas Adicionais**
- **📊 Análise da Petição:** Visualizar dados extraídos
- **🔍 Contexto RAG:** Ver chunks recuperados
- **⚙️ Estatísticas:** Info sobre o vector store

---

## 📁 Estrutura do Projeto

```
rag_contestacoes/
│
├── app.py                          # Aplicação Streamlit principal
│
├── config/
│   ├── __init__.py
│   ├── settings.py                 # Configurações centralizadas
│   └── prompts.py                  # Templates de prompts
│
├── modules/
│   ├── __init__.py
│   ├── document_processor.py      # Processar petição inicial
│   ├── rag_retriever.py           # Busca vetorial RAG
│   ├── llm_generator.py           # Geração via Claude
│   └── validator.py               # Validação e formatação
│
├── outputs/                        # Contestações geradas
│
├── logs/                           # Logs do sistema
│
├── requirements.txt                # Dependências Python
│
├── .env                            # Variáveis de ambiente (criar)
├── .env.example                    # Template .env
│
└── README.md                       # Este arquivo
```

---

## 🧠 Metodologia RAG

### **Chunking Hierárquico Multi-Nível**

O sistema utiliza uma estratégia de chunking hierárquico em 3 níveis:

#### **Nível 1: Contexto Global** (Metadata)
- **Objetivo:** Identificar contestações similares por tipo de caso
- **Conteúdo:** Metadata com informações gerais do documento
- **Top-k:** 10 documentos
- **Uso:** Classificação do tipo de caso + contexto geral

#### **Nível 2: Seções Processuais** (Chunks Semânticos)
- **Objetivo:** Recuperar seções relevantes de contestações
- **Conteúdo:** Blocos por seção (DOS FATOS, DO DIREITO, etc)
- **Top-k:** 20 chunks
- **Uso:** Estrutura argumentativa e fundamentação

#### **Nível 3: Chunks Atômicos** (Precedentes e Artigos)
- **Objetivo:** Recuperar citações específicas
- **Conteúdo:** Precedentes, artigos de lei, argumentos específicos
- **Top-k:** 15 chunks
- **Uso:** Fundamentação legal precisa

### **Estratégia de Busca**

1. **Embedding da Petição:** Gera embedding da petição completa
2. **Classificação:** Identifica tipo de caso via similarity search (Nível 1)
3. **Busca Hierárquica:**
   - Busca paralela nos 3 níveis
   - Filtro por tipo de caso identificado
   - Threshold de similaridade por nível
4. **Síntese:** Organiza e rankeia chunks recuperados
5. **Prompt Engineering:** Constrói prompt estruturado com contexto

### **Vantagens**
- ✅ **Precisão:** Recupera informações em múltiplas granularidades
- ✅ **Relevância:** Filtragem por tipo de caso
- ✅ **Eficiência:** Busca vetorial otimizada
- ✅ **Qualidade:** Contexto rico e estruturado

---

## 💰 Custos

### **Claude Sonnet 4.5 (via API)**

| Componente | Preço | Típico por Contestação |
|-----------|-------|----------------------|
| **Input** | $15/MTok | ~10k tokens = $0.15 |
| **Output** | $75/MTok | ~12k tokens = $0.90 |
| **Total** | - | **~$1.05 por contestação** |

### **Otimizações de Custo**
- Ajustar `max_tokens` conforme necessidade
- Reduzir top-k dos níveis RAG
- Cache de contextos frequentes (futuro)

---

## 🛠️ Desenvolvimento

### **Testar Módulos Individualmente**

```python
# Testar processador de petição
from modules.document_processor import ProcessadorPeticao

processador = ProcessadorPeticao()
dados = processador.processar_arquivo(Path("peticao.pdf"))
print(dados)

# Testar retriever RAG
from modules.rag_retriever import RAGRetriever

retriever = RAGRetriever()
resultado = retriever.retrieval_hierarquico("texto da petição")
print(f"Chunks recuperados: {resultado['total_chunks']}")

# Testar gerador
from modules.llm_generator import LLMGenerator

generator = LLMGenerator()
resultado = generator.gerar_contestacao(dados_peticao, contexto)
print(resultado['contestacao'][:500])
```

### **Adicionar Novo Tipo de Caso**

1. Edite `config/settings.py` → `TIPOS_CASO`
2. Adicione nova entrada com keywords e descrição
3. Regenere vector store com novos documentos do tipo

### **Ajustar Prompts**

Edite `config/prompts.py` para modificar:
- System prompt do Claude
- Estrutura do prompt do usuário
- Formatação do contexto RAG

### **Testes**

```bash
pytest tests/
```

---

## 📊 Métricas de Qualidade

O sistema valida automaticamente:

| Métrica | Descrição | Ideal |
|---------|-----------|-------|
| **Completude Estrutural** | % seções obrigatórias presentes | 100% |
| **Citações Legais** | Número de artigos citados | 5+ |
| **Menções Jurisprudência** | Referências a precedentes | 3+ |
| **Conectivos Argumentativos** | Qualidade da argumentação | 5+ |
| **Score Geral** | Pontuação agregada (0-100) | 80+ |

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie branch para feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças
4. Push para branch
5. Abra Pull Request

---

## 📄 Licença

Projeto proprietário - Uso interno

---

## 👤 Autor

**Pedro**  
Sistema desenvolvido com Claude 4

---

## 📞 Suporte

Para questões ou problemas:
- 📧 Email: [email]
- 💬 Slack: #rag-juridico

---

## 🔄 Changelog

### v1.0.0 (Novembro 2025)
- ✅ Implementação inicial
- ✅ RAG hierárquico 3 níveis
- ✅ Integração Claude Sonnet 4.5
- ✅ Interface Streamlit
- ✅ Validação e formatação DOCX
- ✅ 5 tipos de caso suportados

---

**🏛️ Sistema RAG - Geração Automática de Contestações Jurídicas**  
*Tecnologia a serviço do Direito*
