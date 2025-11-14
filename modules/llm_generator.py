"""
═══════════════════════════════════════════════════════════════════════════
CONTEXT BUILDER + LLM GENERATOR
═══════════════════════════════════════════════════════════════════════════
Constrói contexto RAG otimizado e gera contestação via Claude API
"""

import os
from typing import Dict, List, Optional
import anthropic

from config.settings import Config
from config.prompts import SYSTEM_PROMPT, construir_prompt_usuario

class ContextBuilder:
    """Constrói contexto RAG otimizado para o prompt"""
    
    def __init__(self):
        pass
    
    def construir_contexto(
        self,
        dados_peticao: Dict,
        resultado_rag: Dict
    ) -> Dict:
        """
        Organiza e otimiza o contexto RAG para geração
        
        Args:
            dados_peticao: Dados estruturados da petição inicial
            resultado_rag: Resultado do retrieval hierárquico
            
        Returns:
            Contexto estruturado pronto para o prompt
        """
        # Adicionar classificação aos dados da petição
        classificacao = resultado_rag['classificacao']
        dados_peticao['tipo_caso'] = classificacao['tipo_caso']
        dados_peticao['confianca'] = classificacao['confianca']
        
        # Organizar chunks por nível
        contexto = {
            'nivel_1': self._rankear_chunks(resultado_rag['nivel_1'])[:5],  # Top 5
            'nivel_2': self._rankear_chunks(resultado_rag['nivel_2'])[:10],  # Top 10
            'nivel_3': self._rankear_chunks(resultado_rag['nivel_3'])[:8],  # Top 8
            'especificos': self._extrair_chunks_especificos(
                resultado_rag['nivel_2'],
                dados_peticao['tipo_caso']
            )
        }
        
        return contexto
    
    def _rankear_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """Reordena chunks por relevância (já vêm ordenados, mas pode refinar)"""
        # Já vêm ordenados por similaridade, mas podemos aplicar reranking adicional
        return chunks
    
    def _extrair_chunks_especificos(
        self,
        chunks_nivel_2: List[Dict],
        tipo_caso: str
    ) -> List[Dict]:
        """Extrai chunks com argumentos específicos do tipo de caso"""
        # Filtrar chunks que são do tipo de caso identificado
        especificos = [
            chunk for chunk in chunks_nivel_2
            if chunk['metadata'].get('tipo_lit') == tipo_caso
        ]
        return especificos[:5]  # Top 5


class LLMGenerator:
    """Gera contestação usando Claude API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa gerador
        
        Args:
            api_key: Chave API Anthropic (usa variável de ambiente se None)
        """
        self.api_key = api_key or Config.ANTHROPIC_API_KEY
        
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY não encontrada. "
                "Configure a variável de ambiente ou passe como parâmetro."
            )
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def gerar_contestacao(
        self,
        dados_peticao: Dict,
        contexto_rag: Dict,
        temperatura: float = Config.DEFAULT_TEMPERATURE,
        top_k: int = Config.DEFAULT_TOP_K,
        max_tokens: int = Config.DEFAULT_MAX_TOKENS
    ) -> Dict:
        """
        Gera contestação via Claude API
        
        Args:
            dados_peticao: Dados estruturados da petição
            contexto_rag: Contexto RAG construído
            temperatura: Parâmetro de temperatura (0.3-0.9)
            top_k: Parâmetro top-k (20-60)
            max_tokens: Tokens máximos para geração
            
        Returns:
            Dict com contestação gerada e metadados
        """
        print("\n" + "="*80)
        print("🤖 GERANDO CONTESTAÇÃO COM CLAUDE SONNET 4.5")
        print("="*80 + "\n")
        
        # Validar parâmetros
        temperatura = max(Config.MIN_TEMPERATURE, min(temperatura, Config.MAX_TEMPERATURE))
        top_k = max(Config.MIN_TOP_K, min(top_k, Config.MAX_TOP_K))
        
        print(f"⚙️  Parâmetros:")
        print(f"   Temperatura: {temperatura}")
        print(f"   Top-k: {top_k}")
        print(f"   Max tokens: {max_tokens}\n")
        
        # Construir prompts
        print("📝 Construindo prompts...")
        prompt_usuario = construir_prompt_usuario(dados_peticao, contexto_rag)
        
        # Estimar tokens (aproximado)
        tokens_estimados = (len(SYSTEM_PROMPT) + len(prompt_usuario)) // 4
        print(f"   Tokens estimados (input): ~{tokens_estimados:,}\n")
        
        # Chamar API
        print("🌐 Chamando API Claude...")
        try:
            response = self.client.messages.create(
                model=Config.CLAUDE_MODEL,
                max_tokens=max_tokens,
                temperature=temperatura,
                top_k=top_k,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": prompt_usuario}
                ]
            )
            
            # Extrair resposta
            contestacao_texto = response.content[0].text
            
            # Metadados da geração
            metadados = {
                'model': Config.CLAUDE_MODEL,
                'temperatura': temperatura,
                'top_k': top_k,
                'input_tokens': response.usage.input_tokens,
                'output_tokens': response.usage.output_tokens,
                'stop_reason': response.stop_reason,
                'tipo_caso': dados_peticao.get('tipo_caso'),
                'confianca_classificacao': dados_peticao.get('confianca')
            }
            
            print(f"✅ Geração concluída!")
            print(f"   Input tokens: {metadados['input_tokens']:,}")
            print(f"   Output tokens: {metadados['output_tokens']:,}")
            print(f"   Total tokens: {metadados['input_tokens'] + metadados['output_tokens']:,}\n")
            
            # Custo estimado (aproximado para Sonnet 4.5)
            custo_input = (metadados['input_tokens'] / 1_000_000) * 15  # $15/MTok
            custo_output = (metadados['output_tokens'] / 1_000_000) * 75  # $75/MTok
            custo_total = custo_input + custo_output
            
            print(f"💰 Custo estimado: ${custo_total:.4f}\n")
            
            print("="*80)
            print("✅ CONTESTAÇÃO GERADA COM SUCESSO")
            print("="*80 + "\n")
            
            return {
                'contestacao': contestacao_texto,
                'metadados': metadados,
                'custo_estimado': custo_total,
                'sucesso': True
            }
            
        except anthropic.APIError as e:
            print(f"❌ Erro na API: {e}\n")
            return {
                'contestacao': None,
                'erro': str(e),
                'sucesso': False
            }
        except Exception as e:
            print(f"❌ Erro inesperado: {e}\n")
            return {
                'contestacao': None,
                'erro': str(e),
                'sucesso': False
            }
    
    def regenerar_com_ajustes(
        self,
        resultado_anterior: Dict,
        ajustes: str,
        temperatura: Optional[float] = None,
        top_k: Optional[int] = None
    ) -> Dict:
        """
        Regenera contestação com ajustes solicitados pelo usuário
        
        Args:
            resultado_anterior: Resultado da geração anterior
            ajustes: Instruções de ajuste do usuário
            temperatura: Nova temperatura (opcional)
            top_k: Novo top-k (opcional)
            
        Returns:
            Nova contestação gerada
        """
        # TODO: Implementar funcionalidade de regeneração com feedback
        pass
