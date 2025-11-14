"""
═══════════════════════════════════════════════════════════════════════════
CONFIGURAÇÕES DO SISTEMA RAG - GERAÇÃO DE CONTESTAÇÕES
═══════════════════════════════════════════════════════════════════════════
"""

from pathlib import Path
import os

# Carregar variáveis de ambiente do arquivo .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv não instalado. Execute: pip install python-dotenv")
    print("   Ou configure ANTHROPIC_API_KEY como variável de ambiente do sistema")

class Config:
    """Configurações centralizadas do sistema"""
    
    # ═══════════════════════════════════════════════════════════════════════
    # DIRETÓRIOS
    # ═══════════════════════════════════════════════════════════════════════
    
    # Diretório base (ajustar conforme necessário)
    BASE_DIR = Path(r"c:\users\pbm_s\onedrive\rag pimenta")
    
    # Vector Store
    VECTOR_STORE_DIR = BASE_DIR / "output_rag" / "vector_store"
    
    # Outputs
    OUTPUT_DIR = Path("./outputs")
    LOGS_DIR = Path("./logs")
    
    # ═══════════════════════════════════════════════════════════════════════
    # MODELO DE EMBEDDINGS
    # ═══════════════════════════════════════════════════════════════════════
    
    EMBEDDING_MODEL = "intfloat/multilingual-e5-large"
    EMBEDDING_DIM = 1024
    
    # ═══════════════════════════════════════════════════════════════════════
    # VECTOR STORE
    # ═══════════════════════════════════════════════════════════════════════
    
    COLLECTION_NAME = "contestacoes_juridicas_v1"
    DISTANCE_METRIC = "cosine"
    
    # ═══════════════════════════════════════════════════════════════════════
    # RAG - PARÂMETROS DE RETRIEVAL
    # ═══════════════════════════════════════════════════════════════════════
    
    # Busca por nível hierárquico
    RETRIEVAL_CONFIG = {
        'nivel_1': {  # Contexto global
            'top_k': 10,
            'min_similarity': 0.70,
            'peso': 0.4
        },
        'nivel_2': {  # Seções processuais
            'top_k': 20,
            'min_similarity': 0.65,
            'peso': 0.35
        },
        'nivel_3': {  # Chunks atômicos
            'top_k': 15,
            'min_similarity': 0.60,
            'peso': 0.25
        }
    }
    
    # Limite de tokens para contexto
    MAX_CONTEXT_TOKENS = 12000
    
    # ═══════════════════════════════════════════════════════════════════════
    # CLAUDE API
    # ═══════════════════════════════════════════════════════════════════════
    
    # Modelo
    CLAUDE_MODEL = "claude-sonnet-4-5-20250929"
    
    # Parâmetros padrão
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_TOP_K = 40
    DEFAULT_MAX_TOKENS = 16000
    
    # Limites
    MIN_TEMPERATURE = 0.3
    MAX_TEMPERATURE = 0.9
    MIN_TOP_K = 20
    MAX_TOP_K = 60
    
    # API Key (será lida de variável de ambiente)
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # ═══════════════════════════════════════════════════════════════════════
    # CLASSIFICAÇÃO DE TIPOS DE CASO
    # ═══════════════════════════════════════════════════════════════════════
    
    TIPOS_CASO = {
        'AVISO_PREVIO': {
            'nome': 'Aviso Prévio / Cancelamento',
            'keywords': ['aviso prévio', 'cancelamento', 'rescisão unilateral'],
            'descricao': 'Cancelamento de plano sem aviso prévio adequado'
        },
        'DEMORA_AUTORIZACAO': {
            'nome': 'Demora na Autorização',
            'keywords': ['demora', 'autorização', 'prazo', 'urgência'],
            'descricao': 'Demora excessiva em autorizar procedimentos'
        },
        'HOME_CARE': {
            'nome': 'Home Care / Internação Domiciliar',
            'keywords': ['home care', 'atendimento domiciliar', 'internação domiciliar'],
            'descricao': 'Negativa de cobertura de home care'
        },
        'REEMBOLSO': {
            'nome': 'Reembolso / Divergência de Valores',
            'keywords': ['reembolso', 'pagamento', 'divergência', 'valor'],
            'descricao': 'Problemas com reembolso de despesas médicas'
        },
        'TERAPIAS_REDE': {
            'nome': 'Terapias / Livre Escolha',
            'keywords': ['terapia', 'livre escolha', 'área de abrangência', 'rede credenciada'],
            'descricao': 'Restrições na escolha de profissionais/terapias'
        }
    }
    
    # Limite mínimo de confiança para classificação
    MIN_CONFIDENCE_CLASSIFICATION = 0.70
    
    # ═══════════════════════════════════════════════════════════════════════
    # VALIDAÇÃO E QUALIDADE
    # ═══════════════════════════════════════════════════════════════════════
    
    # Seções obrigatórias em uma contestação
    SECOES_OBRIGATORIAS = [
        'IDENTIFICAÇÃO',
        'MÉRITO',
        'DOS FATOS',
        'DO DIREITO',
        'PEDIDOS'
    ]
    
    # Limites de tamanho
    MIN_CONTESTACAO_LENGTH = 2000  # caracteres
    MAX_CONTESTACAO_LENGTH = 50000  # caracteres
    
    # ═══════════════════════════════════════════════════════════════════════
    # INTERFACE
    # ═══════════════════════════════════════════════════════════════════════
    
    # Título da aplicação
    APP_TITLE = "🏛️ Gerador Automático de Contestações Jurídicas"
    
    # Descrição
    APP_DESCRIPTION = """
    Sistema RAG para geração automática de contestações em ações de planos de saúde.
    Utiliza Claude Sonnet 4.5 e recuperação hierárquica de conhecimento jurídico.
    """
    
    # Formatos de arquivo aceitos
    ALLOWED_FILE_TYPES = ['pdf', 'docx', 'txt']
    
    # Tamanho máximo de upload (MB)
    MAX_FILE_SIZE_MB = 10
    
    @classmethod
    def validar_configuracao(cls):
        """Valida se todas as configurações necessárias estão presentes"""
        erros = []
        
        # Verificar diretórios
        if not cls.VECTOR_STORE_DIR.exists():
            erros.append(f"Vector store não encontrado: {cls.VECTOR_STORE_DIR}")
        
        # Verificar API Key
        if not cls.ANTHROPIC_API_KEY:
            erros.append("ANTHROPIC_API_KEY não configurada. Configure a variável de ambiente.")
        
        # Criar diretórios de saída se não existirem
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        return erros
    
    @classmethod
    def get_tipo_caso_info(cls, tipo_caso: str):
        """Retorna informações sobre um tipo de caso"""
        return cls.TIPOS_CASO.get(tipo_caso, {
            'nome': 'Desconhecido',
            'descricao': 'Tipo de caso não identificado'
        })
