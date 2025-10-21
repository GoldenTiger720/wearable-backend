#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Professional PDF Generator for LIA Core™ Documentation
Converts markdown documentation to professional Brazilian Portuguese PDFs
"""

from weasyprint import HTML, CSS
from datetime import datetime
import re

# Brazilian Portuguese translations
TRANSLATIONS = {
    # Headers
    "LIA Core™ Conversational Module Documentation": "Documentação do Módulo Conversacional LIA Core™",
    "Overview": "Visão Geral",
    "Features": "Recursos",
    "Architecture": "Arquitetura",
    "API Endpoints": "Endpoints da API",
    "Biosignal Context": "Contexto de Biosinais",
    "Example Use Cases": "Exemplos de Casos de Uso",
    "Technical Details": "Detalhes Técnicos",
    "Security Considerations": "Considerações de Segurança",
    "Future Enhancements": "Melhorias Futuras",
    "Interactive Documentation": "Documentação Interativa",

    # CURL Examples
    "LIA Core™ - cURL Command Examples": "LIA Core™ - Exemplos de Comandos cURL",
    "Quick reference guide for testing the LIA Core™ Conversational Module using curl commands.":
        "Guia de referência rápida para testar o Módulo Conversacional LIA Core™ usando comandos curl.",
    "Basic Health Status Chat": "Conversa Básica sobre Estado de Saúde",
    "Ask About Specific Metrics": "Perguntar Sobre Métricas Específicas",
    "Heart Rate Variability (HRV)": "Variabilidade da Frequência Cardíaca (VFC)",
    "Blood Oxygen (SpO2)": "Oxigênio no Sangue (SpO2)",
    "Circadian Rhythm": "Ritmo Circadiano",
    "Wellness Score": "Pontuação de Bem-Estar",
    "General Health Questions (Without Current Data)": "Perguntas Gerais de Saúde (Sem Dados Atuais)",
    "Conversation Management": "Gerenciamento de Conversas",
    "Get Conversation History": "Obter Histórico de Conversas",
    "Clear Conversation History": "Limpar Histórico de Conversas",
    "Get Current Biosignal Data": "Obter Dados Atuais de Biosinais",
    "System Status": "Status do Sistema",
    "Multi-turn Conversation Example": "Exemplo de Conversa Multi-turno",
    "Pretty Print JSON Responses": "Formatar Respostas JSON",
    "Extract Just the Response Message": "Extrair Apenas a Mensagem de Resposta",
    "Useful One-Liners": "Comandos Úteis de Uma Linha",
    "Interactive API Documentation": "Documentação Interativa da API",

    # Content translations
    "The": "O",
    "is an advanced AI-powered chat interface": "é uma interface de chat avançada alimentada por IA",
    "that provides natural language interaction": "que fornece interação em linguagem natural",
    "Natural Language Health Analysis": "Análise de Saúde em Linguagem Natural",
    "Ask questions about your health in plain English and receive personalized insights":
        "Faça perguntas sobre sua saúde em linguagem simples e receba insights personalizados",
    "Real-time Biosignal Context": "Contexto de Biosinais em Tempo Real",
    "has access to your current heart rate": "tem acesso à sua frequência cardíaca atual",
    "Conversational Memory": "Memória Conversacional",
    "Maintains conversation context across multiple messages within a session":
        "Mantém o contexto da conversa através de múltiplas mensagens dentro de uma sessão",
    "Multi-dimensional Insights": "Insights Multidimensionais",
    "Analyzes data from all three proprietary layers": "Analisa dados de todas as três camadas proprietárias",
    "Personalized Recommendations": "Recomendações Personalizadas",
    "Provides actionable health advice based on your current state":
        "Fornece conselhos de saúde acionáveis com base no seu estado atual",
    "Flexible Context Mode": "Modo de Contexto Flexível",
    "Chat with or without biosignal data depending on your needs":
        "Converse com ou sem dados de biosinais dependendo de suas necessidades",

    # API sections
    "Chat with LIA": "Conversar com LIA",
    "Engage in a conversation with LIA about your health.": "Participe de uma conversa com LIA sobre sua saúde.",
    "Request Body:": "Corpo da Requisição:",
    "Response:": "Resposta:",
    "Example with curl:": "Exemplo com curl:",

    # Technical terms
    "User Message": "Mensagem do Usuário",
    "LIA Chat Engine": "Motor de Chat LIA",
    "Signal Quality": "Qualidade do Sinal",
    "HRV & Frequency": "VFC & Frequência",
    "LIA Insights": "Insights da LIA",
    "AI-Powered Response": "Resposta Alimentada por IA",

    # Biosignal sections
    "Raw Signals": "Sinais Brutos",
    "Heart Rate (BPM)": "Frequência Cardíaca (BPM)",
    "Blood Oxygen Saturation (SpO2 %)": "Saturação de Oxigênio no Sangue (SpO2 %)",
    "Body Temperature (°C)": "Temperatura Corporal (°C)",
    "Activity Level (steps/min)": "Nível de Atividade (passos/min)",

    # Details sections
    "AI Model": "Modelo de IA",
    "Model": "Modelo",
    "Provider": "Provedor",
    "Temperature": "Temperatura",
    "balanced creativity and consistency": "equilíbrio entre criatividade e consistência",
    "Max Tokens": "Tokens Máximos",
    "per response": "por resposta",
    "Timeout": "Tempo Limite",
    "seconds": "segundos",
    "Max Retries": "Tentativas Máximas",

    "Conversation Management": "Gerenciamento de Conversas",
    "History Size": "Tamanho do Histórico",
    "messages per session": "mensagens por sessão",
    "last": "últimas",
    "exchanges": "trocas",
    "Session Isolation": "Isolamento de Sessão",
    "Each session_id maintains separate conversation context":
        "Cada session_id mantém contexto de conversa separado",
    "Memory Scope": "Escopo de Memória",
    "In-memory storage (resets on server restart)": "Armazenamento em memória (reinicia ao reiniciar o servidor)",

    "System Prompt": "Prompt do Sistema",
    "is configured with a detailed system prompt that defines:":
        "está configurado com um prompt de sistema detalhado que define:",
    "Personality": "Personalidade",
    "Professional, warm, evidence-based": "Profissional, caloroso, baseado em evidências",
    "Capabilities": "Capacidades",
    "Health analysis, metric interpretation, recommendations":
        "Análise de saúde, interpretação de métricas, recomendações",
    "Limitations": "Limitações",
    "Never diagnoses medical conditions": "Nunca diagnostica condições médicas",
    "Response Style": "Estilo de Resposta",
    "Concise, clear, actionable": "Conciso, claro, acionável",

    # Security
    "API Key": "Chave da API",
    "Store OPENAI_API_KEY securely in environment variables, never commit to version control":
        "Armazene OPENAI_API_KEY com segurança em variáveis de ambiente, nunca faça commit no controle de versão",
    "Rate Limiting": "Limitação de Taxa",
    "Consider implementing rate limiting for production use":
        "Considere implementar limitação de taxa para uso em produção",
    "Authentication": "Autenticação",
    "Add user authentication before deploying to production":
        "Adicione autenticação de usuário antes de implantar em produção",
    "Data Privacy": "Privacidade de Dados",
    "Conversation history contains health data - implement appropriate data retention policies":
        "Histórico de conversas contém dados de saúde - implemente políticas apropriadas de retenção de dados",
    "Use HTTPS in production to encrypt data in transit":
        "Use HTTPS em produção para criptografar dados em trânsito",

    # Future
    "Potential improvements for the LIA Chat Engine:": "Melhorias potenciais para o Motor de Chat LIA:",
    "Persistent conversation storage in PostgreSQL database":
        "Armazenamento persistente de conversas em banco de dados PostgreSQL",
    "Long-term trend analysis from historical biosignal data":
        "Análise de tendências de longo prazo a partir de dados históricos de biosinais",
    "Multi-language support": "Suporte multi-idioma",
    "Voice input/output integration": "Integração de entrada/saída de voz",
    "Personalized health coaching programs": "Programas personalizados de coaching de saúde",
    "Integration with external health APIs (Apple Health, Google Fit)":
        "Integração com APIs de saúde externas (Apple Health, Google Fit)",
    "Export conversation history to PDF reports": "Exportar histórico de conversas para relatórios em PDF",
    "Custom AI model fine-tuning on health domain data":
        "Fine-tuning personalizado do modelo de IA com dados do domínio de saúde",

    # Footer
    "Powered by OpenAI GPT-4o-mini": "Alimentado por OpenAI GPT-4o-mini",
    "Integrated with": "Integrado com",
    "proprietary biosignal processing layers": "camadas proprietárias de processamento de biosinais",

    # Notes and misc
    "Note": "Nota",
    "All examples assume the server is running on": "Todos os exemplos assumem que o servidor está rodando em",
    "Instead of curl, you can also test the API using the interactive Swagger UI:":
        "Em vez de curl, você também pode testar a API usando a interface Swagger interativa:",
    "Open in browser": "Abrir no navegador",
    "This provides a web interface where you can:": "Isso fornece uma interface web onde você pode:",
    "See all available endpoints": "Ver todos os endpoints disponíveis",
    "Test requests directly in the browser": "Testar requisições diretamente no navegador",
    "View request/response schemas": "Visualizar esquemas de requisição/resposta",
    "Try different parameters": "Experimentar diferentes parâmetros",

    "Once the server is running, visit:": "Uma vez que o servidor esteja rodando, visite:",
    "Swagger UI": "Interface Swagger",

    "Health Status Check": "Verificação de Estado de Saúde",
    "Understanding Metrics": "Entendendo as Métricas",
    "Activity Recommendations": "Recomendações de Atividade",
    "General Health Advice (without current data)": "Aconselhamento Geral de Saúde (sem dados atuais)",
    "The server will display:": "O servidor exibirá:",
}

def translate_text(text):
    """Translate text to Brazilian Portuguese"""
    result = text
    for en, pt in sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True):
        result = result.replace(en, pt)
    return result

def translate_markdown(md_content):
    """Translate markdown content while preserving code blocks"""
    lines = md_content.split('\n')
    translated_lines = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            translated_lines.append(line)
            continue

        if in_code_block or line.strip().startswith('http'):
            translated_lines.append(line)
        else:
            translated_lines.append(translate_text(line))

    return '\n'.join(translated_lines)

CSS_STYLE = """
@page {
    size: A4;
    margin: 2.5cm 2cm;
    @bottom-right {
        content: "Página " counter(page);
        font-family: Arial, sans-serif;
        font-size: 9pt;
        color: #666;
    }
}

body {
    font-family: Georgia, serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
}

h1 {
    color: #1a4d8f;
    font-size: 24pt;
    margin-bottom: 20pt;
    padding-bottom: 10pt;
    border-bottom: 3px solid #1a4d8f;
}

h2 {
    color: #2563ab;
    font-size: 18pt;
    margin-top: 24pt;
    margin-bottom: 12pt;
}

h3 {
    color: #3b7fc4;
    font-size: 14pt;
    margin-top: 18pt;
    margin-bottom: 10pt;
}

code {
    font-family: Courier New, monospace;
    font-size: 9pt;
    background-color: #f5f5f5;
    padding: 2pt 4pt;
    color: #c7254e;
}

pre {
    font-family: Courier New, monospace;
    font-size: 8.5pt;
    background-color: #f8f8f8;
    border-left: 4px solid #1a4d8f;
    padding: 10pt;
    margin: 10pt 0;
    page-break-inside: avoid;
}

pre code {
    background-color: transparent;
    padding: 0;
    color: #333;
}

.header {
    text-align: center;
    margin-bottom: 30pt;
    padding: 20pt;
    background: #1a4d8f;
    color: white;
}

.header h1 {
    color: white;
    border-bottom: none;
    margin: 0;
}

.footer {
    margin-top: 30pt;
    padding-top: 15pt;
    border-top: 2px solid #1a4d8f;
    text-align: center;
    font-size: 9pt;
    color: #666;
}
"""

def markdown_to_html(md_content, title):
    """Convert markdown to HTML"""
    import markdown2

    html_body = markdown2.markdown(
        md_content,
        extras=['fenced-code-blocks', 'tables', 'header-ids']
    )

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
    </div>
    <div style="text-align: right; font-size: 9pt; color: #666; margin-bottom: 20pt;">
        Gerado em: {datetime.now().strftime('%d/%m/%Y')}
    </div>
    {html_body}
    <div class="footer">
        <p><strong>LIA Core™</strong> - Sistema de Monitoramento de Biosinais</p>
    </div>
</body>
</html>"""
    return html

def generate_pdf(md_file, output_pdf, title):
    """Generate PDF from markdown"""
    print(f"Processando: {md_file}")

    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    print(f"Traduzindo para Português...")
    translated_md = translate_markdown(md_content)

    print(f"Convertendo para HTML...")
    html_content = markdown_to_html(translated_md, title)

    print(f"Gerando PDF...")
    HTML(string=html_content).write_pdf(
        output_pdf,
        stylesheets=[CSS(string=CSS_STYLE)]
    )

    print(f"PDF criado: {output_pdf}\n")

def main():
    """Main function"""
    print("=" * 60)
    print("LIA Core - Gerador de PDFs")
    print("=" * 60)
    print()

    generate_pdf(
        md_file='/home/administrator/Documents/wearable/backend/LIA_CHAT_README.md',
        output_pdf='/home/administrator/Documents/wearable/backend/LIA_CHAT_README_PT-BR.pdf',
        title='Documentação do Módulo Conversacional LIA Core™'
    )

    generate_pdf(
        md_file='/home/administrator/Documents/wearable/backend/CURL_EXAMPLES.md',
        output_pdf='/home/administrator/Documents/wearable/backend/CURL_EXAMPLES_PT-BR.pdf',
        title='LIA Core™ - Exemplos de Comandos cURL'
    )

    print("=" * 60)
    print("PDFs gerados com sucesso!")
    print("=" * 60)

if __name__ == '__main__':
    main()
