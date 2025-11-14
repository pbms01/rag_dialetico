"""
═══════════════════════════════════════════════════════════════════════════
PROCESSADOR DE PETIÇÃO INICIAL
═══════════════════════════════════════════════════════════════════════════
Extrai e estrutura informações da petição inicial para alimentar o RAG
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
import PyPDF2
import docx

class ProcessadorPeticao:
    """Processa petição inicial e extrai informações estruturadas"""
    
    def __init__(self):
        self.texto_completo = ""
        self.dados_estruturados = {}
    
    def processar_arquivo(self, arquivo_path: Path) -> Dict:
        """
        Processa arquivo de petição e retorna dados estruturados
        
        Args:
            arquivo_path: Caminho do arquivo (PDF, DOCX ou TXT)
            
        Returns:
            Dicionário com dados estruturados da petição
        """
        # Extrair texto baseado no tipo de arquivo
        extensao = arquivo_path.suffix.lower()
        
        if extensao == '.pdf':
            self.texto_completo = self._extrair_texto_pdf(arquivo_path)
        elif extensao == '.docx':
            self.texto_completo = self._extrair_texto_docx(arquivo_path)
        elif extensao == '.txt':
            self.texto_completo = arquivo_path.read_text(encoding='utf-8')
        else:
            raise ValueError(f"Formato não suportado: {extensao}")
        
        # Extrair informações estruturadas
        self.dados_estruturados = self._estruturar_dados()
        
        return self.dados_estruturados
    
    def _extrair_texto_pdf(self, pdf_path: Path) -> str:
        """Extrai texto de PDF"""
        texto = []
        
        try:
            with open(pdf_path, 'rb') as arquivo:
                leitor = PyPDF2.PdfReader(arquivo)
                for pagina in leitor.pages:
                    texto.append(pagina.extract_text())
        except Exception as e:
            raise Exception(f"Erro ao ler PDF: {e}")
        
        return "\n\n".join(texto)
    
    def _extrair_texto_docx(self, docx_path: Path) -> str:
        """Extrai texto de DOCX"""
        try:
            doc = docx.Document(docx_path)
            texto = [paragrafo.text for paragrafo in doc.paragraphs if paragrafo.text.strip()]
            return "\n\n".join(texto)
        except Exception as e:
            raise Exception(f"Erro ao ler DOCX: {e}")
    
    def _estruturar_dados(self) -> Dict:
        """Extrai informações estruturadas do texto"""
        
        dados = {
            'texto_completo': self.texto_completo,
            'autor': self._extrair_autor(),
            'reu': self._extrair_reu(),
            'numero_processo': self._extrair_numero_processo(),
            'elementos_facticos': self._extrair_elementos_facticos(),
            'pedidos': self._extrair_pedidos(),
            'valor_causa': self._extrair_valor_causa(),
            'documentos_anexos': self._extrair_documentos_anexos()
        }
        
        return dados
    
    def _extrair_autor(self) -> str:
        """Extrai nome do autor da petição"""
        # Padrões comuns
        padroes = [
            r'(?:Autor|Requerente|Impetrante):\s*([^\n]+)',
            r'(?:vem\s+)?([A-ZÀ-Ú][a-zà-ú]+(?:\s+[A-ZÀ-Ú][a-zà-ú]+)+),?\s+(?:brasileiro|brasileiro\(a\)|nacionalidade)',
            r'([A-ZÀ-Ú][a-zà-ú]+(?:\s+[A-ZÀÚ][a-zà-ú]+)+),?\s+(?:portador|portadora)'
        ]
        
        for padrao in padroes:
            match = re.search(padrao, self.texto_completo, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Não identificado"
    
    def _extrair_reu(self) -> str:
        """Extrai nome do réu"""
        # Padrões comuns
        padroes = [
            r'(?:Réu|Requerido|Impetrado):\s*([^\n]+)',
            r'(?:contra|em\s+face\s+(?:de|da))\s+([A-Z][A-Z\s]+(?:LTDA|S\.?A\.?|COOPERATIVA)?)',
            r'(UNIMED[^\n,\.]+)'
        ]
        
        for padrao in padroes:
            match = re.search(padrao, self.texto_completo, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Padrão: UNIMED
        if 'UNIMED' in self.texto_completo.upper():
            return "UNIMED FERJ"
        
        return "Não identificado"
    
    def _extrair_numero_processo(self) -> Optional[str]:
        """Extrai número do processo"""
        # Padrão CNJ: NNNNNNN-DD.AAAA.J.TR.OOOO
        padrao = r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}'
        match = re.search(padrao, self.texto_completo)
        
        if match:
            return match.group(0)
        
        return None
    
    def _extrair_elementos_facticos(self) -> List[str]:
        """Extrai os principais fatos alegados"""
        elementos = []
        
        # Procurar seção "DOS FATOS"
        match_fatos = re.search(
            r'(?:DOS?\s+FATOS?|HISTÓRICO|NARRATIVA)[:\s]*(.+?)(?=DOS?\s+DIREITOS?|FUNDAMENTAÇÃO|DO\s+PEDIDO|$)',
            self.texto_completo,
            re.IGNORECASE | re.DOTALL
        )
        
        if match_fatos:
            secao_fatos = match_fatos.group(1)
            
            # Dividir em parágrafos
            paragrafos = [p.strip() for p in secao_fatos.split('\n\n') if len(p.strip()) > 50]
            elementos = paragrafos[:10]  # Limitar a 10 elementos principais
        
        # Se não encontrou seção específica, extrair primeiros parágrafos substantivos
        if not elementos:
            paragrafos = self.texto_completo.split('\n\n')
            elementos = [p.strip() for p in paragrafos if len(p.strip()) > 100][:5]
        
        return elementos
    
    def _extrair_pedidos(self) -> List[str]:
        """Extrai os pedidos formulados"""
        pedidos = []
        
        # Procurar seção "DOS PEDIDOS" ou "REQUER"
        match_pedidos = re.search(
            r'(?:DOS?\s+PEDIDOS?|REQUER|REQUERIMENTOS?)[:\s]*(.+?)(?=NESTES\s+TERMOS|VALOR\s+DA\s+CAUSA|$)',
            self.texto_completo,
            re.IGNORECASE | re.DOTALL
        )
        
        if match_pedidos:
            secao_pedidos = match_pedidos.group(1)
            
            # Encontrar itens numerados ou com alíneas
            itens = re.findall(
                r'(?:[a-z]\)|[ivx]+\)|\d+\.|\d+\))\s*([^\n]+)',
                secao_pedidos,
                re.IGNORECASE
            )
            
            if itens:
                pedidos = [item.strip() for item in itens]
            else:
                # Se não tem numeração, pegar frases que começam com verbos típicos
                frases = re.findall(
                    r'((?:seja|sejam|determine|condene|declare)[^\.\n]+\.)',
                    secao_pedidos,
                    re.IGNORECASE
                )
                pedidos = [f.strip() for f in frases]
        
        return pedidos
    
    def _extrair_valor_causa(self) -> Optional[str]:
        """Extrai valor da causa"""
        # Padrões comuns
        padroes = [
            r'(?:VALOR\s+DA\s+CAUSA|DÁ-SE\s+À\s+CAUSA)[:\s]*R?\$?\s*([\d\.,]+)',
            r'R\$\s*([\d\.,]+)\s*\(.*?\)',  # Valor por extenso
        ]
        
        for padrao in padroes:
            match = re.search(padrao, self.texto_completo, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extrair_documentos_anexos(self) -> List[str]:
        """Lista documentos anexos mencionados"""
        documentos = []
        
        # Padrões comuns
        match = re.search(
            r'(?:DOCUMENTOS?|ANEXOS?|INSTRUI)[:\s]*(.+?)(?=\n\n|$)',
            self.texto_completo,
            re.IGNORECASE | re.DOTALL
        )
        
        if match:
            secao_docs = match.group(1)
            itens = re.findall(r'(?:[a-z]\)|\d+\.)\s*([^\n]+)', secao_docs, re.IGNORECASE)
            documentos = [item.strip() for item in itens if item.strip()]
        
        return documentos
    
    def get_texto_para_embedding(self) -> str:
        """Retorna texto otimizado para geração de embedding"""
        # Combinar elementos principais para embedding mais relevante
        partes = [
            self.dados_estruturados.get('autor', ''),
            self.dados_estruturados.get('reu', ''),
        ]
        
        # Adicionar resumo dos fatos (primeiros 3)
        fatos = self.dados_estruturados.get('elementos_facticos', [])[:3]
        partes.extend(fatos)
        
        # Adicionar pedidos (primeiros 2)
        pedidos = self.dados_estruturados.get('pedidos', [])[:2]
        partes.extend(pedidos)
        
        texto_embedding = " | ".join([p for p in partes if p])
        
        # Limitar tamanho (para eficiência do embedding)
        if len(texto_embedding) > 2000:
            texto_embedding = texto_embedding[:2000]
        
        return texto_embedding
