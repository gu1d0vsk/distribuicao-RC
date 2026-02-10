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
        return None, "A data de início deve ser anterior ou igual à data de fim."
    
    total_dias = (fim - inicio).days + 1
    
    ano_inicial = inicio.year
    ano_final = fim.year
    
    distribuicao_dias = {}
    
    # 1. Calcular dias por ano
    for ano in range(ano_inicial, ano_final + 1):
        inicio_periodo = max(inicio, date(ano, 1, 1))
        fim_periodo = min(fim, date(ano, 12, 31))
        dias_no_ano = (fim_periodo - inicio_periodo).days + 1
        distribuicao_dias[ano] = dias_no_ano

    # 2. Calcular valor financeiro proporcional
    resultado_final = {}
    soma_valores = 0.0
    maior_valor = -1
    ano_maior_valor = -1

    for ano, dias in distribuicao_dias.items():
        # Calcula a proporção precisa
        proporcao = dias / total_dias
        # Calcula o valor monetário e arredonda para 2 casas
        valor_ano = round(proporcao * valor_total, 2)
        
        resultado_final[ano] = valor_ano
        soma_valores += valor_ano
        
        # Rastreia o maior valor para ajuste de centavos
        if valor_ano > maior_valor:
            maior_valor = valor_ano
            ano_maior_valor = ano
            
    # 3. Ajuste fino de centavos (para a soma bater exatamente o valor total)
    diferenca = round(valor_total - soma_valores, 2)
    
    if diferenca != 0:
        resultado_final[ano_maior_valor] += diferenca
        resultado_final[ano_maior_valor] = round(resultado_final[ano_maior_valor], 2)

    return resultado_final, None

# --- Interface ---

st.markdown('<p class="main-title">Distribuição Orçamentária</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Calcule os valores anuais do contrato</p>', unsafe_allow_html=True)

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
    dados, erro = calcular_distribuicao_financeira(dt_inicio, dt_fim, valor_input)
    
    if erro:
        st.markdown(f'<div class="custom-warning">{erro}</div>', unsafe_allow_html=True)
    else:
        cards_html = ""
        for ano, valor in dados.items():
            valor_formatado = formatar_moeda(valor)
            # HTML sem indentação para evitar bugs de renderização
            cards_html += f"""
<div class="metric-custom metric-year">
    <div class="label">Ano {ano}</div>
    <div class="value">{valor_formatado}</div>
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
