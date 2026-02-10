import streamlit as st
import datetime
from datetime import date
import streamlit.components.v1 as components

# --- Configuração da Página ---
st.set_page_config(page_title="Calculadora de Orçamento", page_icon="💰", layout="centered")

# --- CSS / Identidade Visual ---
page_bg_img = """
<style>
[data-testid="stApp"] {
    background-image: linear-gradient(rgb(2, 45, 44) 0%, rgb(0, 21, 21) 100%);
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}

/* Força texto claro */
.stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label, span, div {
    color: #e0e0e0 !important;
}

/* CSS "NUCLEAR" PARA LIMPAR A INTERFACE */
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
[data-testid="stStatusWidget"] {display:none;}

/* Container Principal */
.main .block-container { 
    max-width: 800px; 
    padding-bottom: 5rem;
    transform: translateY(0);
    transition: transform 0.2s cubic-bezier(0.25, 1, 0.5, 1);
}

.main-title { font-size: 2.2rem !important; font-weight: bold; text-align: center; }
.sub-title { color: gray; text-align: center; font-size: 1.25rem !important; margin-bottom: 2rem; }

/* Inputs */
div[data-testid="stDateInput"] input, div[data-testid="stNumberInput"] input { 
    border-radius: 1.5rem !important; 
    text-align: center; 
    font-weight: 600; 
}
.main div[data-testid="stDateInput"] > label, .main div[data-testid="stNumberInput"] > label { 
    text-align: center !important; 
    width: 100%; 
    display: block; 
}

/* Botões com efeito NEON */
div[data-testid="stButton"] > button { 
    background-color: rgb(221, 79, 5) !important; 
    color: #FFFFFF !important; 
    border-radius: 4rem; 
    border-color: transparent;
    transition: all 0.3s ease; 
    font-weight: bold;
}
div[data-testid="stButton"] > button:hover {
    box-shadow: 0 0 12px rgba(221, 79, 5, 0.8), 0 0 20px rgba(221, 79, 5, 0.4); 
    transform: scale(1.02);
}

/* Cards de Resultado */
.section-container { text-align: center; margin-top: 1.5rem; }
.results-grid { 
    display: grid; 
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
    gap: 1rem; 
    margin-top: 1rem;
}

.metric-custom { 
    background-color: #F0F2F6; 
    border-radius: 1.5rem; 
    padding: 1rem; 
    text-align: center; 
    display: flex; 
    flex-direction: column; 
    justify-content: center; 
    color: #31333f !important; 
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

.metric-year { background-color: rgb(0, 80, 81); }

/* Ajuste específico para textos dentro dos cards */
.metric-year .value { color: #FFFFFF !important; font-size: 1.6rem; font-weight: 900; }
.metric-year .label { color: rgba(255, 255, 255, 0.85) !important; font-size: 1rem; margin-bottom: 0.25rem; }
.metric-year .details { color: rgba(255, 255, 255, 0.7) !important; font-size: 0.9rem; margin-top: 0.25rem; font-weight: 500; }

.custom-warning {
    border-radius: 1.5rem;
    padding: 1rem;
    margin-top: 1rem;
    text-align: center;
    background-color: rgba(255, 170, 0, 0.1); 
    border: 1px solid rgba(255, 170, 0, 0.5); 
    color: rgb(247, 185, 61) !important;
}

/* Animação */
.results-container { animation: fadeIn 0.5s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# --- Funções de Lógica ---

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def calcular_distribuicao_financeira(inicio, fim, valor_total):
    if inicio > fim:
        return None, None, "A data de início deve ser anterior ou igual à data de fim."
    
    total_dias = (fim - inicio).days + 1
    
    ano_inicial = inicio.year
    ano_final = fim.year
    
    # 1. Calcular dias por ano
    distribuicao_dias = {}
    for ano in range(ano_inicial, ano_final + 1):
        inicio_periodo = max(inicio, date(ano, 1, 1))
        fim_periodo = min(fim, date(ano, 12, 31))
        dias_no_ano = (fim_periodo - inicio_periodo).days + 1
        distribuicao_dias[ano] = dias_no_ano

    # 2. Calcular PROPORÇÃO FIXA (2 casas decimais)
    proporcoes_finais = {}
    soma_proporcoes = 0.0
    ano_maior_dias = -1
    maior_dias = -1

    for ano, dias in distribuicao_dias.items():
        # Arredonda a proporção para 2 casas imediatamente
        prop = round(dias / total_dias, 2)
        proporcoes_finais[ano] = prop
        soma_proporcoes += prop
        
        # Rastreia o ano com mais dias para receber o ajuste de arredondamento da proporção
        if dias > maior_dias:
            maior_dias = dias
            ano_maior_dias = ano
            
    # Ajuste para soma das proporções ser 1.00
    diferenca_prop = round(1.00 - soma_proporcoes, 2)
    if diferenca_prop != 0:
        proporcoes_finais[ano_maior_dias] += diferenca_prop
        proporcoes_finais[ano_maior_dias] = round(proporcoes_finais[ano_maior_dias], 2)

    # 3. Calcular VALOR MONETÁRIO baseado na proporção fixa
    valores_finais = {}
    soma_valores = 0.0
    
    for ano, prop in proporcoes_finais.items():
        val = round(prop * valor_total, 2)
        valores_finais[ano] = val
        soma_valores += val
        
    # Ajuste de centavos (se a multiplicação das proporções gerar dízima em dinheiro)
    diferenca_valor = round(valor_total - soma_valores, 2)
    if diferenca_valor != 0:
        # Aplica a diferença de centavos no mesmo ano que tem a maior fatia
        valores_finais[ano_maior_dias] += diferenca_valor
        valores_finais[ano_maior_dias] = round(valores_finais[ano_maior_dias], 2)

    return valores_finais, proporcoes_finais, None

# --- Interface ---

st.markdown('<p class="main-title">Distribuição Orçamentária</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Calcule os valores anuais pela proporção fixa</p>', unsafe_allow_html=True)

# Input de Valor
valor_input = st.number_input("Valor da Compra (R$)", min_value=0.0, value=10000.0, step=100.0, format="%.2f")

col1, col2 = st.columns(2)

with col1:
    dt_inicio = st.date_input("Início da Vigência", value=date.today(), format="DD/MM/YYYY")

with col2:
    dt_fim = st.date_input("Fim da Vigência", value=date.today() + datetime.timedelta(days=365), format="DD/MM/YYYY")

col_vazia_esq, col_btn, col_vazia_dir = st.columns([1, 2, 1])

with col_btn:
    calcular = st.button("Calcular Valores", use_container_width=True)

# --- Processamento ---

if calcular:
    valores, proporcoes, erro = calcular_distribuicao_financeira(dt_inicio, dt_fim, valor_input)
    
    if erro:
        st.markdown(f'<div class="custom-warning">{erro}</div>', unsafe_allow_html=True)
    else:
        cards_html = ""
        for ano in valores.keys():
            val = valores[ano]
            prop = proporcoes[ano]
            
            valor_formatado = formatar_moeda(val)
            # Exibe a proporção exata usada no cálculo
            fator_str = f"{prop:.2f}"
            
            cards_html += f"""
<div class="metric-custom metric-year">
    <div class="label">Ano {ano}</div>
    <div class="value">{valor_formatado}</div>
    <div class="details">Fator: {fator_str}</div>
</div>"""
        
        valor_total_fmt = formatar_moeda(valor_input)
        
        final_html = f"""
<div class="results-container">
    <div class="section-container">
        <h3>Resultado da Distribuição</h3>
        <p style="font-size: 0.9rem; opacity: 0.8;">Valor Total: {valor_total_fmt}</p>
        <div class="results-grid">
            {cards_html}
        </div>
    </div>
</div>
"""
        st.markdown(final_html, unsafe_allow_html=True)

# --- Scripts de Limpeza ---
js_cleaner = """
<script>
    const removeStreamlitElements = () => {
        const footer = window.parent.document.querySelector('footer');
        if (footer) { footer.style.display = 'none'; }
        
        const badge = window.parent.document.querySelector('div[class*="viewerBadge"]');
        if (badge) { badge.style.display = 'none'; }
    }
    removeStreamlitElements();
    const observer = new MutationObserver(() => {
        removeStreamlitElements();
    });
    observer.observe(window.parent.document.body, { childList: true, subtree: true });
</script>
"""
components.html(js_cleaner, height=0)
