"""
═══════════════════════════════════════════════════════════════════════════
INTERFACE STREAMLIT - GERADOR DE CONTESTAÇÕES
═══════════════════════════════════════════════════════════════════════════
Aplicação web para geração automática de contestações jurídicas
"""

import streamlit as st
from pathlib import Path
from datetime import datetime
import json

from config.settings import Config
from modules.document_processor import ProcessadorPeticao
from modules.rag_retriever import RAGRetriever
from modules.llm_generator import ContextBuilder, LLMGenerator
from modules.validator import ValidadorContestacao, FormatadorDOCX

# Configuração da página
st.set_page_config(
    page_title="Gerador de Contestações",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f4788;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f4788;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def inicializar_sessao():
    """Inicializa variáveis de sessão"""
    if 'processador' not in st.session_state:
        st.session_state.processador = ProcessadorPeticao()
    
    if 'retriever' not in st.session_state:
        with st.spinner("🔄 Carregando sistema RAG..."):
            st.session_state.retriever = RAGRetriever()
    
    if 'generator' not in st.session_state:
        st.session_state.generator = LLMGenerator()
    
    if 'builder' not in st.session_state:
        st.session_state.builder = ContextBuilder()
    
    if 'validador' not in st.session_state:
        st.session_state.validador = ValidadorContestacao()
    
    if 'formatador' not in st.session_state:
        st.session_state.formatador = FormatadorDOCX()
    
    if 'resultado' not in st.session_state:
        st.session_state.resultado = None


def validar_configuracao():
    """Valida configuração do sistema"""
    erros = Config.validar_configuracao()
    
    if erros:
        st.error("❌ **Erros de Configuração:**")
        for erro in erros:
            st.error(f"   • {erro}")
        st.stop()


def interface_principal():
    """Interface principal da aplicação"""
    
    # Cabeçalho
    st.markdown(f'<div class="main-header">{Config.APP_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">{Config.APP_DESCRIPTION}</div>', unsafe_allow_html=True)
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Gerar Contestação",
        "📊 Análise da Petição",
        "🔍 Contexto RAG",
        "⚙️ Estatísticas do Sistema"
    ])
    
    # ==================================================================
    # TAB 1: GERAR CONTESTAÇÃO
    # ==================================================================
    with tab1:
        st.header("📁 Upload da Petição Inicial")
        
        arquivo = st.file_uploader(
            "Selecione o arquivo da petição inicial",
            type=Config.ALLOWED_FILE_TYPES,
            help=f"Formatos aceitos: {', '.join(Config.ALLOWED_FILE_TYPES).upper()}"
        )
        
        if arquivo:
            # Salvar temporariamente
            temp_path = Path("./temp") / arquivo.name
            
            # Criar diretório temp se não existir
            temp_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(temp_path, 'wb') as f:
                f.write(arquivo.getvalue())
            
            st.success(f"✅ Arquivo carregado: {arquivo.name}")
            
            # Configurações de geração
            st.header("⚙️ Configurações de Geração")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                temperatura = st.slider(
                    "🌡️ Temperatura",
                    min_value=float(Config.MIN_TEMPERATURE),
                    max_value=float(Config.MAX_TEMPERATURE),
                    value=float(Config.DEFAULT_TEMPERATURE),
                    step=0.1,
                    help="Controla a criatividade. Menor = mais conservadora, Maior = mais criativa"
                )
            
            with col2:
                top_k = st.slider(
                    "🎯 Top-k",
                    min_value=Config.MIN_TOP_K,
                    max_value=Config.MAX_TOP_K,
                    value=Config.DEFAULT_TOP_K,
                    step=5,
                    help="Controla a diversidade vocabular. Menor = mais focada, Maior = mais diversa"
                )
            
            with col3:
                max_tokens = st.number_input(
                    "📊 Max Tokens",
                    min_value=8000,
                    max_value=20000,
                    value=Config.DEFAULT_MAX_TOKENS,
                    step=1000,
                    help="Tamanho máximo da contestação gerada"
                )
            
            # Opções avançadas
            with st.expander("🔧 Opções Avançadas"):
                mostrar_analise = st.checkbox("Mostrar análise detalhada da petição", value=True)
                mostrar_rag = st.checkbox("Mostrar chunks RAG recuperados", value=False)
                mostrar_metricas = st.checkbox("Mostrar métricas de qualidade", value=True)
            
            st.divider()
            
            # Botão de geração
            if st.button("🚀 GERAR CONTESTAÇÃO", type="primary", use_container_width=True):
                
                with st.spinner("🔄 Processando..."):
                    try:
                        # 1. Processar petição
                        st.info("📄 Processando petição inicial...")
                        dados_peticao = st.session_state.processador.processar_arquivo(temp_path)
                        
                        # 2. Retrieval RAG
                        st.info("🔍 Executando retrieval RAG...")
                        texto_query = st.session_state.processador.get_texto_para_embedding()
                        resultado_rag = st.session_state.retriever.retrieval_hierarquico(texto_query)
                        
                        # 3. Construir contexto
                        st.info("📚 Construindo contexto...")
                        contexto = st.session_state.builder.construir_contexto(
                            dados_peticao,
                            resultado_rag
                        )
                        
                        # 4. Gerar contestação
                        st.info("🤖 Gerando contestação com Claude...")
                        resultado = st.session_state.generator.gerar_contestacao(
                            dados_peticao,
                            contexto,
                            temperatura=temperatura,
                            top_k=top_k,
                            max_tokens=max_tokens
                        )
                        
                        if resultado['sucesso']:
                            # 5. Validar
                            validacao = st.session_state.validador.validar(resultado['contestacao'])
                            
                            # 6. Salvar resultado na sessão
                            st.session_state.resultado = {
                                'contestacao': resultado['contestacao'],
                                'metadados': resultado['metadados'],
                                'validacao': validacao,
                                'dados_peticao': dados_peticao,
                                'contexto_rag': contexto,
                                'resultado_rag_completo': resultado_rag,
                                'custo': resultado['custo_estimado']
                            }
                            
                            st.success("✅ Contestação gerada com sucesso!")
                            st.rerun()
                        
                        else:
                            st.error(f"❌ Erro na geração: {resultado.get('erro', 'Erro desconhecido')}")
                    
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())
            
            # Mostrar resultado se existir
            if st.session_state.resultado:
                st.divider()
                st.header("📄 Resultado")
                
                res = st.session_state.resultado
                
                # Informações gerais
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Tipo de Caso",
                        res['dados_peticao'].get('tipo_caso', 'N/A')
                    )
                
                with col2:
                    conf = res['dados_peticao'].get('confianca', 0)
                    st.metric(
                        "Confiança",
                        f"{conf:.1%}"
                    )
                
                with col3:
                    st.metric(
                        "Tokens",
                        f"{res['metadados']['output_tokens']:,}"
                    )
                
                with col4:
                    st.metric(
                        "Custo",
                        f"${res['custo']:.4f}"
                    )
                
                # Métricas de qualidade
                if mostrar_metricas:
                    st.subheader("📊 Métricas de Qualidade")
                    
                    val = res['validacao']
                    met = val['metricas']
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Score Geral", f"{met['score_qualidade']}/100")
                    
                    with col2:
                        st.metric("Classificação", met['classificacao'])
                    
                    with col3:
                        st.metric("Citações Legais", met['citacoes_legais'])
                    
                    with col4:
                        st.metric("Completude", f"{met['completude_estrutural']:.0%}")
                    
                    # Alertas
                    if val['alertas']:
                        st.warning("⚠️ **Alertas:**")
                        for alerta in val['alertas']:
                            st.warning(f"   {alerta}")
                
                # Contestação
                st.subheader("📜 Contestação Gerada")
                st.text_area(
                    "Texto da contestação",
                    value=res['contestacao'],
                    height=500,
                    label_visibility="collapsed"
                )
                
                # Botões de ação
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📥 Download DOCX", use_container_width=True):
                        # Gerar DOCX
                        output_path = Config.OUTPUT_DIR / f"contestacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
                        Config.OUTPUT_DIR.mkdir(exist_ok=True)
                        
                        st.session_state.formatador.criar_docx(
                            res['contestacao'],
                            res['metadados'],
                            output_path
                        )
                        
                        # Download
                        with open(output_path, 'rb') as f:
                            st.download_button(
                                "⬇️ Baixar DOCX",
                                data=f.read(),
                                file_name=output_path.name,
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                use_container_width=True
                            )
                
                with col2:
                    if st.button("📋 Copiar Texto", use_container_width=True):
                        st.code(res['contestacao'], language=None)
                        st.info("✅ Texto disponível para copiar acima")
                
                with col3:
                    if st.button("🔄 Nova Geração", use_container_width=True):
                        st.session_state.resultado = None
                        st.rerun()
    
    # ==================================================================
    # TAB 2: ANÁLISE DA PETIÇÃO
    # ==================================================================
    with tab2:
        st.header("📊 Análise da Petição Inicial")
        
        if st.session_state.resultado:
            dados = st.session_state.resultado['dados_peticao']
            
            # Partes
            st.subheader("⚖️ Partes")
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Autor:** {dados.get('autor', 'Não identificado')}")
            with col2:
                st.info(f"**Réu:** {dados.get('reu', 'Não identificado')}")
            
            # Elementos factuais
            st.subheader("📋 Elementos Factuais")
            fatos = dados.get('elementos_facticos', [])
            if fatos:
                for i, fato in enumerate(fatos, 1):
                    st.write(f"{i}. {fato[:200]}...")
            else:
                st.write("Nenhum elemento factual identificado")
            
            # Pedidos
            st.subheader("🎯 Pedidos")
            pedidos = dados.get('pedidos', [])
            if pedidos:
                for i, pedido in enumerate(pedidos, 1):
                    st.write(f"{i}. {pedido}")
            else:
                st.write("Nenhum pedido identificado")
            
            # Valor da causa
            if dados.get('valor_causa'):
                st.subheader("💰 Valor da Causa")
                st.info(f"R$ {dados['valor_causa']}")
        
        else:
            st.info("👆 Faça o upload de uma petição na aba 'Gerar Contestação' para ver a análise")
    
    # ==================================================================
    # TAB 3: CONTEXTO RAG
    # ==================================================================
    with tab3:
        st.header("🔍 Contexto RAG Recuperado")
        
        if st.session_state.resultado:
            rag = st.session_state.resultado['resultado_rag_completo']
            
            st.metric("Total de Chunks Recuperados", rag['total_chunks'])
            
            # Nível 1
            with st.expander(f"📚 Nível 1 - Contexto Global ({len(rag['nivel_1'])} chunks)"):
                for i, chunk in enumerate(rag['nivel_1'][:5], 1):
                    st.write(f"**Chunk {i}** (Sim: {chunk['similaridade']:.2%})")
                    st.code(chunk['conteudo'][:300] + "...", language=None)
            
            # Nível 2
            with st.expander(f"📄 Nível 2 - Seções Processuais ({len(rag['nivel_2'])} chunks)"):
                for i, chunk in enumerate(rag['nivel_2'][:5], 1):
                    st.write(f"**Chunk {i}** (Sim: {chunk['similaridade']:.2%})")
                    st.write(f"Seção: {chunk['metadata'].get('secao', 'N/A')}")
                    st.code(chunk['conteudo'][:250] + "...", language=None)
            
            # Nível 3
            with st.expander(f"⚖️ Nível 3 - Chunks Atômicos ({len(rag['nivel_3'])} chunks)"):
                for i, chunk in enumerate(rag['nivel_3'][:5], 1):
                    st.write(f"**Chunk {i}** (Sim: {chunk['similaridade']:.2%})")
                    st.code(chunk['conteudo'][:200] + "...", language=None)
        
        else:
            st.info("👆 Gere uma contestação primeiro para ver o contexto RAG")
    
    # ==================================================================
    # TAB 4: ESTATÍSTICAS DO SISTEMA
    # ==================================================================
    with tab4:
        st.header("📊 Estatísticas do Sistema RAG")
        
        stats = st.session_state.retriever.get_estatisticas()
        
        st.metric("Total de Chunks no Vector Store", f"{stats['total_chunks']:,}")
        
        # Por nível
        st.subheader("📈 Distribuição por Nível")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Nível 1", stats['por_nivel'].get('nivel_1', 0))
        with col2:
            st.metric("Nível 2", stats['por_nivel'].get('nivel_2', 0))
        with col3:
            st.metric("Nível 3", stats['por_nivel'].get('nivel_3', 0))
        
        # Por tipo
        st.subheader("📋 Distribuição por Tipo de Caso")
        for tipo, count in stats['por_tipo'].items():
            info_tipo = Config.get_tipo_caso_info(tipo)
            st.write(f"**{info_tipo['nome']}:** {count} chunks")
        
        # Informações do modelo
        st.subheader("🤖 Configuração")
        st.json({
            "Embedding Model": Config.EMBEDDING_MODEL,
            "Claude Model": Config.CLAUDE_MODEL,
            "Collection": Config.COLLECTION_NAME,
            "Vector Store": str(Config.VECTOR_STORE_DIR)
        })


def main():
    """Função principal"""
    
    # Validar configuração
    validar_configuracao()
    
    # Inicializar sessão
    inicializar_sessao()
    
    # Interface
    interface_principal()
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/1f4788/FFFFFF?text=RAG+Juridico", use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("### ℹ️ Sobre")
        st.markdown("""
        Sistema RAG para geração automática de contestações jurídicas.
        
        **Tecnologias:**
        - Claude Sonnet 4.5
        - ChromaDB
        - Multilingual-E5-Large
        - Streamlit
        """)
        
        st.markdown("---")
        
        st.markdown("### 📚 Documentação")
        st.markdown("""
        - [Guia de Uso](#)
        - [Metodologia RAG](#)
        - [API Reference](#)
        """)
        
        st.markdown("---")
        
        st.markdown(f"**Versão:** 1.0.0  \n**Data:** {datetime.now().strftime('%d/%m/%Y')}")


if __name__ == "__main__":
    main()
