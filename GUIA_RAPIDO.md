# 🚀 GUIA RÁPIDO DE INÍCIO

## ⚡ Start Rápido (5 minutos)

### 1️⃣ Instalação

```bash
# Execute o script de setup
setup.bat

# Aguarde a instalação das dependências (~3-5 minutos)
```

### 2️⃣ Configuração

```bash
# Edite o arquivo .env e adicione sua API key:
ANTHROPIC_API_KEY=sk-ant-api03-XXXXXXXXXXXXXXXX

# Obtenha sua key em: https://console.anthropic.com/settings/keys
```

### 3️⃣ Executar

```bash
# Execute a aplicação
run.bat

# OU manualmente:
streamlit run app.py
```

### 4️⃣ Usar

1. Abra: `http://localhost:8501`
2. Faça upload da petição inicial (PDF/DOCX/TXT)
3. Ajuste parâmetros (opcional):
   - **Temperatura:** 0.7 (recomendado)
   - **Top-k:** 40 (recomendado)
4. Clique em **"🚀 GERAR CONTESTAÇÃO"**
5. Aguarde ~20-35 segundos
6. Download do DOCX ou copie o texto

---

## 📋 Checklist Pré-Execução

- [ ] Python 3.10+ instalado
- [ ] Setup executado (`setup.bat`)
- [ ] Arquivo `.env` configurado com `ANTHROPIC_API_KEY`
- [ ] Vector store presente em: `c:\users\pbm_s\onedrive\rag pimenta\output_rag\vector_store`

---

## ⚠️ Troubleshooting Comum

### Erro: "ANTHROPIC_API_KEY não configurada"
**Solução:** Edite `.env` e adicione sua API key

### Erro: "Vector store não encontrado"
**Solução:** Verifique se o caminho em `config/settings.py` está correto

### Erro: ModuleNotFoundError
**Solução:** Execute `pip install -r requirements.txt` novamente

### Interface não abre
**Solução:** Verifique se a porta 8501 está livre

---

## 💰 Custos Estimados

| Ação | Custo Estimado |
|------|----------------|
| Gerar 1 contestação | ~$1.05 |
| Gerar 10 contestações | ~$10.50 |
| Gerar 100 contestações | ~$105.00 |

---

## 📞 Suporte

- 📖 Documentação completa: `README.md`
- 🐛 Problemas: Abra issue ou contate o administrador
- 💬 Dúvidas: Consulte a equipe técnica

---

## 🎯 Dicas de Uso

### Para Melhores Resultados:

1. **Petições Claras:** Quanto mais estruturada a petição inicial, melhor o resultado
2. **Temperatura:**
   - Use 0.5-0.7 para casos "padrão"
   - Use 0.7-0.8 para casos mais complexos
3. **Revisão:** SEMPRE revise a contestação gerada antes de usar
4. **Métricas:** Preste atenção no "Score de Qualidade" - idealmente 80+

### O Que Fazer se a Qualidade Estiver Baixa:

1. Verifique se o tipo de caso foi classificado corretamente
2. Tente regenerar com temperatura diferente
3. Se necessário, adicione mais contexto manualmente
4. Considere treinar o modelo com mais exemplos do tipo de caso

---

**🏛️ Sistema RAG - Gerador de Contestações**  
Versão 1.0.0 | Novembro 2025
