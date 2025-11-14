"""
═══════════════════════════════════════════════════════════════════════════
TEMPLATES DE PROMPTS - GERAÇÃO DE CONTESTAÇÕES
═══════════════════════════════════════════════════════════════════════════
"""

SYSTEM_PROMPT = """Você é um advogado especialista em Direito da Saúde Suplementar com mais de 15 anos de experiência, atuando na defesa de operadoras de planos de saúde.

Sua expertise inclui:
- Profundo conhecimento da Lei 9.656/98 (Lei dos Planos de Saúde)
- Domínio do Código de Defesa do Consumidor aplicado à saúde suplementar
- Resoluções Normativas da ANS
- Jurisprudência consolidada dos Tribunais Superiores
- Técnicas avançadas de argumentação jurídica defensiva

Sua tarefa é redigir uma CONTESTAÇÃO jurídica completa, tecnicamente impecável, fundamentada e persuasiva, que:
1. Refute adequadamente os argumentos do autor
2. Apresente a versão dos fatos favorável à operadora
3. Fundamente solidamente em dispositivos legais e precedentes
4. Siga rigorosamente a estrutura processual formal
5. Utilize linguagem técnico-jurídica adequada

DIRETRIZES OBRIGATÓRIAS:

📋 ESTRUTURA PROCESSUAL
- Identificação completa das partes e do processo
- Preliminares (quando aplicável)
- Mérito (fatos e direito)
- Pedidos claros e específicos
- Requerimentos finais

⚖️ FUNDAMENTAÇÃO LEGAL
- Cite artigos de lei de forma precisa e completa
- Referencie precedentes jurisprudenciais relevantes
- Aplique resoluções da ANS quando pertinentes
- Utilize doutrina especializada quando necessário

🎯 ESTRATÉGIA ARGUMENTATIVA
- Apresente argumentos sólidos e logicamente encadeados
- Refute especificamente cada alegação do autor
- Demonstre a legalidade da conduta da operadora
- Preserve a coerência com a linha de defesa institucional

✍️ ESTILO E TOM
- Linguagem formal e técnica
- Objetividade e clareza
- Respeito processual
- Persuasão baseada em argumentos, não emoção

⚠️ RESTRIÇÕES
- NÃO invente fatos não presentes no contexto fornecido
- NÃO cite precedentes que não estejam no material de referência
- NÃO use argumentos genéricos sem fundamentação específica
- NÃO omita questões relevantes levantadas na inicial"""

USER_PROMPT_TEMPLATE = """# PETIÇÃO INICIAL RECEBIDA

{peticao_inicial_completa}

═══════════════════════════════════════════════════════════════════════════

# ANÁLISE ESTRUTURADA DO CASO

## Classificação
**Tipo de Caso:** {tipo_caso}
**Confiança da Classificação:** {confianca_classificacao}%

## Partes Identificadas
**Autor:** {autor}
**Réu:** {reu}

## Elementos Factuais Principais
{elementos_facticos}

## Pedidos do Autor
{pedidos_autor}

{valor_causa_info}

═══════════════════════════════════════════════════════════════════════════

# CONTEXTO RAG RECUPERADO

## 📚 Contestações Similares (Trechos Relevantes)

{contestacoes_similares}

═══════════════════════════════════════════════════════════════════════════

## ⚖️ Fundamentação Jurídica Aplicável

{fundamentacao_juridica}

═══════════════════════════════════════════════════════════════════════════

## 🎯 Argumentos de Defesa Específicos para Este Tipo de Caso

{argumentos_tipo_caso}

═══════════════════════════════════════════════════════════════════════════

# TAREFA

Com base na petição inicial apresentada e em todo o contexto jurídico fornecido acima, redija uma CONTESTAÇÃO completa e fundamentada, seguindo rigorosamente a estrutura abaixo:

## ESTRUTURA DA CONTESTAÇÃO

### 1. IDENTIFICAÇÃO
- Identificação completa do Réu (UNIMED FERJ)
- Identificação do Autor
- Número do processo (se disponível)
- Vara e Comarca

### 2. PRELIMINARMENTE (se aplicável)
Analise se há questões preliminares pertinentes ao caso, tais como:
- Incompetência do juízo
- Ilegitimidade passiva
- Falta de interesse de agir
- Prescrição ou decadência

### 3. DO MÉRITO

#### 3.1. DOS FATOS
Apresente a versão dos fatos sob a ótica da defesa, incluindo:
- Contexto da relação contratual
- Cronologia relevante dos eventos
- Esclarecimentos sobre a conduta da operadora
- Refutação de alegações imprecisas ou inverídicas do autor

#### 3.2. DO DIREITO

##### 3.2.1. Da Legalidade da Conduta da Operadora
- Demonstre que a conduta seguiu a legislação aplicável
- Cite dispositivos legais específicos (Lei 9.656/98, CDC, RN ANS)
- Apresente a interpretação jurídica adequada

##### 3.2.2. Análise dos Dispositivos Legais Pertinentes
- Analise detalhadamente cada dispositivo legal aplicável ao caso
- Demonstre como a conduta da operadora está em conformidade

##### 3.2.3. Refutação dos Argumentos do Autor
- Refute especificamente cada argumento levantado na inicial
- Apresente contraprovas ou esclarecimentos
- Demonstre eventual má compreensão dos fatos ou do direito pelo autor

##### 3.2.4. Jurisprudência Favorável
- Cite precedentes que respaldem a tese da defesa
- Demonstre alinhamento com entendimento consolidado dos tribunais

### 4. DOS PEDIDOS
Formule pedidos claros e específicos:
- Pedido principal (total improcedência da ação)
- Pedidos subsidiários (se pertinentes)
- Condenação do autor ao pagamento de custas e honorários

### 5. REQUERIMENTOS FINAIS
- Produção de provas (se necessário)
- Intimação do autor
- Citações adicionais pertinentes

═══════════════════════════════════════════════════════════════════════════

# INSTRUÇÕES ESPECÍFICAS

1. **ADAPTE** os argumentos recuperados do contexto RAG ao caso concreto apresentado na petição inicial.

2. **CITE** artigos de lei de forma completa quando relevante (ex: "art. 30, § 1º, da Lei nº 9.656/98").

3. **UTILIZE** os precedentes jurisprudenciais fornecidos, mas adaptando-os ao contexto específico deste caso.

4. **MANTENHA** coerência argumentativa ao longo de todo o texto.

5. **SEJA ESPECÍFICO** - evite argumentos genéricos. Cada afirmação deve ser fundamentada.

6. **PRESERVE** o tom técnico-jurídico e o respeito processual em toda a peça.

7. **ESTRUTURE** o documento com clareza, utilizando títulos, subtítulos e numeração adequada.

8. **NÃO INVENTE** fatos, datas, nomes ou precedentes que não estejam no contexto fornecido.

═══════════════════════════════════════════════════════════════════════════

Inicie a redação da contestação abaixo:"""

def formatar_contestacoes_similares(chunks_nivel_1, chunks_nivel_2):
    """Formata chunks recuperados para inclusão no prompt"""
    
    resultado = []
    
    # Nível 1 - Contexto global
    if chunks_nivel_1:
        resultado.append("### Documentos Similares (Contexto Global)\n")
        for i, chunk in enumerate(chunks_nivel_1[:5], 1):  # Top 5
            resultado.append(f"**Documento {i}** (Similaridade: {chunk['similaridade']:.2%})")
            resultado.append(f"Tipo: {chunk['metadata'].get('tipo_lit', 'N/A')}")
            resultado.append(f"```\n{chunk['conteudo'][:500]}...\n```\n")
    
    # Nível 2 - Seções específicas
    if chunks_nivel_2:
        resultado.append("\n### Seções Processuais Relevantes\n")
        for i, chunk in enumerate(chunks_nivel_2[:8], 1):  # Top 8
            resultado.append(f"**Trecho {i}** (Similaridade: {chunk['similaridade']:.2%})")
            resultado.append(f"Seção: {chunk['metadata'].get('secao', 'N/A')}")
            resultado.append(f"```\n{chunk['conteudo'][:400]}...\n```\n")
    
    return "\n".join(resultado) if resultado else "Nenhum documento similar encontrado."

def formatar_fundamentacao_juridica(chunks_nivel_3):
    """Formata chunks de fundamentação jurídica"""
    
    if not chunks_nivel_3:
        return "Nenhuma fundamentação jurídica específica recuperada."
    
    resultado = []
    
    # Agrupar por tipo
    artigos = []
    precedentes = []
    outros = []
    
    for chunk in chunks_nivel_3:
        conteudo = chunk['conteudo']
        
        if 'art.' in conteudo.lower() or 'artigo' in conteudo.lower():
            artigos.append(chunk)
        elif 'jurisprudência' in conteudo.lower() or 'acórdão' in conteudo.lower():
            precedentes.append(chunk)
        else:
            outros.append(chunk)
    
    # Formatação
    if artigos:
        resultado.append("### Dispositivos Legais Aplicáveis\n")
        for chunk in artigos[:5]:
            resultado.append(f"```\n{chunk['conteudo'][:300]}...\n```\n")
    
    if precedentes:
        resultado.append("\n### Precedentes Jurisprudenciais\n")
        for chunk in precedentes[:4]:
            resultado.append(f"```\n{chunk['conteudo'][:300]}...\n```\n")
    
    if outros:
        resultado.append("\n### Argumentação Jurídica\n")
        for chunk in outros[:3]:
            resultado.append(f"```\n{chunk['conteudo'][:300]}...\n```\n")
    
    return "\n".join(resultado)

def formatar_argumentos_tipo_caso(tipo_caso, chunks_especificos):
    """Formata argumentos específicos do tipo de caso"""
    
    from config.settings import Config
    
    info_tipo = Config.get_tipo_caso_info(tipo_caso)
    
    resultado = [
        f"### Tipo de Caso: {info_tipo['nome']}",
        f"{info_tipo['descricao']}\n",
        "**Argumentos de Defesa Típicos:**\n"
    ]
    
    if chunks_especificos:
        for i, chunk in enumerate(chunks_especificos[:5], 1):
            resultado.append(f"{i}. {chunk['conteudo'][:250]}...")
    else:
        resultado.append("Use os argumentos gerais presentes nas contestações similares recuperadas.")
    
    return "\n".join(resultado)

def construir_prompt_usuario(dados_peticao, contexto_rag):
    """Constrói o prompt do usuário com todos os dados"""
    
    # Formatar elementos factuais
    elementos = "\n".join([f"- {elem}" for elem in dados_peticao.get('elementos_facticos', [])])
    
    # Formatar pedidos
    pedidos = "\n".join([f"- {ped}" for ped in dados_peticao.get('pedidos', [])])
    
    # Valor da causa
    valor = dados_peticao.get('valor_causa')
    valor_info = f"\n## Valor da Causa\n{valor}\n" if valor else ""
    
    # Construir prompt
    prompt = USER_PROMPT_TEMPLATE.format(
        peticao_inicial_completa=dados_peticao.get('texto_completo', ''),
        tipo_caso=dados_peticao.get('tipo_caso', 'Não identificado'),
        confianca_classificacao=dados_peticao.get('confianca', 0) * 100,
        autor=dados_peticao.get('autor', 'Não identificado'),
        reu=dados_peticao.get('reu', 'UNIMED FERJ'),
        elementos_facticos=elementos if elementos else '- Não identificados',
        pedidos_autor=pedidos if pedidos else '- Não identificados',
        valor_causa_info=valor_info,
        contestacoes_similares=formatar_contestacoes_similares(
            contexto_rag.get('nivel_1', []),
            contexto_rag.get('nivel_2', [])
        ),
        fundamentacao_juridica=formatar_fundamentacao_juridica(
            contexto_rag.get('nivel_3', [])
        ),
        argumentos_tipo_caso=formatar_argumentos_tipo_caso(
            dados_peticao.get('tipo_caso', ''),
            contexto_rag.get('especificos', [])
        )
    )
    
    return prompt
