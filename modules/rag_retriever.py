"""
═══════════════════════════════════════════════════════════════════════════
RAG RETRIEVER - RECUPERAÇÃO HIERÁRQUICA MULTI-NÍVEL
═══════════════════════════════════════════════════════════════════════════
Implementa busca vetorial hierárquica em 3 níveis
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
from pathlib import Path
import numpy as np

from config.settings import Config

class RAGRetriever:
    """Recuperação RAG hierárquica com ChromaDB"""
    
    def __init__(self, vector_store_dir: Optional[Path] = None):
        """
        Inicializa o retriever
        
        Args:
            vector_store_dir: Diretório do vector store (usa Config se None)
        """
        self.vector_store_dir = vector_store_dir or Config.VECTOR_STORE_DIR
        
        # Carregar modelo de embeddings
        print(f"📥 Carregando modelo de embeddings: {Config.EMBEDDING_MODEL}")
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        print("✅ Modelo carregado")
        
        # Conectar ao ChromaDB
        print(f"🔌 Conectando ao vector store: {self.vector_store_dir}")
        self.client = chromadb.PersistentClient(
            path=str(self.vector_store_dir),
            settings=Settings(anonymized_telemetry=False)
        )
        
        self.collection = self.client.get_collection(name=Config.COLLECTION_NAME)
        print(f"✅ Conectado à collection: {Config.COLLECTION_NAME}")
        print(f"📊 Total de chunks: {self.collection.count()}\n")
    
    def gerar_embedding(self, texto: str) -> List[float]:
        """Gera embedding para um texto"""
        embedding = self.embedding_model.encode(
            texto,
            convert_to_numpy=True,
            normalize_embeddings=True  # Normalizar para cosine similarity
        )
        return embedding.tolist()
    
    def buscar_nivel_1(
        self,
        query_embedding: List[float],
        tipo_caso: Optional[str] = None,
        top_k: Optional[int] = None
    ) -> List[Dict]:
        """
        Busca no nível 1 (contexto global)
        
        Args:
            query_embedding: Embedding da query
            tipo_caso: Filtrar por tipo de caso (opcional)
            top_k: Número de resultados (usa Config se None)
            
        Returns:
            Lista de chunks recuperados com metadados
        """
        config = Config.RETRIEVAL_CONFIG['nivel_1']
        top_k = top_k or config['top_k']
        
        # Preparar filtro (ChromaDB requer $and para múltiplos campos)
        if tipo_caso:
            where_filter = {
                '$and': [
                    {'nivel': 1},
                    {'tipo_lit': tipo_caso}
                ]
            }
        else:
            where_filter = {'nivel': 1}
        
        # Buscar
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Processar resultados
        chunks = []
        for doc, meta, dist in zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        ):
            # Converter distância para similaridade (se usando cosine)
            similaridade = 1 - dist if Config.DISTANCE_METRIC == 'cosine' else dist
            
            # Filtrar por similaridade mínima
            if similaridade >= config['min_similarity']:
                chunks.append({
                    'conteudo': doc,
                    'metadata': meta,
                    'similaridade': similaridade,
                    'nivel': 1
                })
        
        return chunks
    
    def buscar_nivel_2(
        self,
        query_embedding: List[float],
        tipo_caso: Optional[str] = None,
        tipo_doc: Optional[str] = None,
        top_k: Optional[int] = None
    ) -> List[Dict]:
        """
        Busca no nível 2 (seções processuais)
        
        Args:
            query_embedding: Embedding da query
            tipo_caso: Filtrar por tipo de caso (opcional)
            tipo_doc: Filtrar por tipo de documento - "inicial" ou "contestacao" (opcional)
            top_k: Número de resultados
            
        Returns:
            Lista de chunks recuperados
        """
        config = Config.RETRIEVAL_CONFIG['nivel_2']
        top_k = top_k or config['top_k']
        
        # Preparar filtro (ChromaDB requer $and para múltiplos campos)
        filters = [{'nivel': 2}]
        
        if tipo_caso:
            filters.append({'tipo_lit': tipo_caso})
        
        if tipo_doc:
            filters.append({'tipo_doc': tipo_doc})
        
        # Usar $and apenas se houver múltiplos filtros
        if len(filters) > 1:
            where_filter = {'$and': filters}
        else:
            where_filter = filters[0]
        
        # Buscar
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Processar resultados
        chunks = []
        for doc, meta, dist in zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        ):
            similaridade = 1 - dist if Config.DISTANCE_METRIC == 'cosine' else dist
            
            if similaridade >= config['min_similarity']:
                chunks.append({
                    'conteudo': doc,
                    'metadata': meta,
                    'similaridade': similaridade,
                    'nivel': 2
                })
        
        return chunks
    
    def buscar_nivel_3(
        self,
        query_embedding: List[float],
        tipo_caso: Optional[str] = None,
        top_k: Optional[int] = None
    ) -> List[Dict]:
        """
        Busca no nível 3 (chunks atômicos - precedentes, artigos de lei)
        
        Args:
            query_embedding: Embedding da query
            tipo_caso: Filtrar por tipo de caso (opcional)
            top_k: Número de resultados
            
        Returns:
            Lista de chunks recuperados
        """
        config = Config.RETRIEVAL_CONFIG['nivel_3']
        top_k = top_k or config['top_k']
        
        # Preparar filtro (ChromaDB requer $and para múltiplos campos)
        if tipo_caso:
            where_filter = {
                '$and': [
                    {'nivel': 3},
                    {'tipo_lit': tipo_caso}
                ]
            }
        else:
            where_filter = {'nivel': 3}
        
        # Buscar
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Processar resultados
        chunks = []
        for doc, meta, dist in zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        ):
            similaridade = 1 - dist if Config.DISTANCE_METRIC == 'cosine' else dist
            
            if similaridade >= config['min_similarity']:
                chunks.append({
                    'conteudo': doc,
                    'metadata': meta,
                    'similaridade': similaridade,
                    'nivel': 3
                })
        
        return chunks
    
    def classificar_tipo_caso(self, query_embedding: List[float]) -> Dict:
        """
        Classifica o tipo de caso baseado em similaridade com nível 1
        
        Args:
            query_embedding: Embedding da petição inicial
            
        Returns:
            Dict com tipo_caso e confiança
        """
        # Buscar top-k documentos nível 1
        chunks_nivel_1 = self.buscar_nivel_1(query_embedding, top_k=10)
        
        if not chunks_nivel_1:
            return {
                'tipo_caso': None,
                'confianca': 0.0,
                'distribuicao': {}
            }
        
        # Contar tipos de litígio
        contagem_tipos = {}
        soma_similaridades = {}
        
        for chunk in chunks_nivel_1:
            tipo = chunk['metadata'].get('tipo_lit', 'DESCONHECIDO')
            sim = chunk['similaridade']
            
            contagem_tipos[tipo] = contagem_tipos.get(tipo, 0) + 1
            soma_similaridades[tipo] = soma_similaridades.get(tipo, 0) + sim
        
        # Calcular scores ponderados (frequência + similaridade média)
        scores = {}
        for tipo in contagem_tipos:
            freq_norm = contagem_tipos[tipo] / len(chunks_nivel_1)
            sim_media = soma_similaridades[tipo] / contagem_tipos[tipo]
            scores[tipo] = (0.5 * freq_norm) + (0.5 * sim_media)
        
        # Tipo com maior score
        tipo_identificado = max(scores, key=scores.get)
        confianca = scores[tipo_identificado]
        
        return {
            'tipo_caso': tipo_identificado,
            'confianca': confianca,
            'distribuicao': scores
        }
    
    def retrieval_hierarquico(
        self,
        query_text: str,
        tipo_caso: Optional[str] = None,
        auto_classificar: bool = True
    ) -> Dict:
        """
        Executa retrieval hierárquico completo em 3 níveis
        
        Args:
            query_text: Texto da query (petição inicial)
            tipo_caso: Tipo de caso (se conhecido). Se None e auto_classificar=True, classifica automaticamente
            auto_classificar: Se True, classifica automaticamente o tipo de caso
            
        Returns:
            Dict com chunks de todos os níveis e metadados
        """
        print("\n" + "="*80)
        print("🔍 INICIANDO RETRIEVAL HIERÁRQUICO")
        print("="*80 + "\n")
        
        # 1. Gerar embedding da query
        print("📊 Gerando embedding da query...")
        query_embedding = self.gerar_embedding(query_text)
        print("✅ Embedding gerado\n")
        
        # 2. Classificar tipo de caso (se necessário)
        if tipo_caso is None and auto_classificar:
            print("🏷️  Classificando tipo de caso...")
            classificacao = self.classificar_tipo_caso(query_embedding)
            tipo_caso = classificacao['tipo_caso']
            confianca = classificacao['confianca']
            
            print(f"✅ Tipo identificado: {tipo_caso}")
            print(f"   Confiança: {confianca:.2%}\n")
            
            if confianca < Config.MIN_CONFIDENCE_CLASSIFICATION:
                print(f"⚠️  Confiança baixa ({confianca:.2%}). Busca sem filtro de tipo.\n")
                tipo_caso = None
        else:
            classificacao = {'tipo_caso': tipo_caso, 'confianca': 1.0}
        
        # 3. Buscar em cada nível
        print("📚 Buscando no Nível 1 (Contexto Global)...")
        chunks_nivel_1 = self.buscar_nivel_1(query_embedding, tipo_caso=tipo_caso)
        print(f"   ✅ {len(chunks_nivel_1)} chunks recuperados\n")
        
        print("📄 Buscando no Nível 2 (Seções Processuais)...")
        chunks_nivel_2 = self.buscar_nivel_2(
            query_embedding,
            tipo_caso=tipo_caso,
            tipo_doc='contestacao'  # Focar em contestações
        )
        print(f"   ✅ {len(chunks_nivel_2)} chunks recuperados\n")
        
        print("⚖️  Buscando no Nível 3 (Chunks Atômicos)...")
        chunks_nivel_3 = self.buscar_nivel_3(query_embedding, tipo_caso=tipo_caso)
        print(f"   ✅ {len(chunks_nivel_3)} chunks recuperados\n")
        
        # 4. Consolidar resultados
        resultado = {
            'classificacao': classificacao,
            'nivel_1': chunks_nivel_1,
            'nivel_2': chunks_nivel_2,
            'nivel_3': chunks_nivel_3,
            'total_chunks': len(chunks_nivel_1) + len(chunks_nivel_2) + len(chunks_nivel_3),
            'query_embedding': query_embedding
        }
        
        print("="*80)
        print(f"✅ RETRIEVAL CONCLUÍDO - Total: {resultado['total_chunks']} chunks")
        print("="*80 + "\n")
        
        return resultado
    
    def get_estatisticas(self) -> Dict:
        """Retorna estatísticas do vector store"""
        stats = {
            'total_chunks': self.collection.count(),
            'por_nivel': {},
            'por_tipo': {}
        }
        
        # Por nível
        for nivel in [1, 2, 3]:
            results = self.collection.get(where={'nivel': nivel})
            stats['por_nivel'][f'nivel_{nivel}'] = len(results['ids'])
        
        # Por tipo de litígio
        for tipo in Config.TIPOS_CASO.keys():
            results = self.collection.get(where={'tipo_lit': tipo})
            stats['por_tipo'][tipo] = len(results['ids'])
        
        return stats
