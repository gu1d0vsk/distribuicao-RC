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
div[data-testid="stDateInput"] input { 
    border-radius: 1.5rem !important; 
    text-align: center; 
    font-weight: 600; 
}
.main div[data-testid="stDateInput"] > label { 
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
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
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
    color: #31333f !important; /* Força cor escura dentro do card claro */
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

.metric-year { background-color: rgb(0, 80, 81); }

/* Ajuste específico para textos dentro dos cards */
.metric-year .value { color: #FFFFFF !important; font-size: 1.8rem; font-weight: 900; }
.metric-year .label { color: rgba(255, 255, 255, 0.85) !important; font-size: 1rem; margin-bottom: 0.25rem; }
.metric-year .details { color: rgba(255, 255, 255, 0.7) !important; font-size: 0.8rem; margin-top: 0.25rem; }

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

def calcular_distribuicao(inicio, fim):
    if inicio > fim:
        return None, "A data de início deve ser anterior ou igual à data de fim."
    
    total_dias = (fim - inicio).days + 1
    
    ano_inicial = inicio.year
    ano_final = fim.year
    
    distribuicao_bruta = {}
    
    for ano in range(ano_inicial, ano_final + 1):
        inicio_periodo = max(inicio, date(ano, 1, 1))
        fim_periodo = min(fim, date(ano, 12, 31))
        dias_no_ano = (fim_periodo - inicio_periodo).days + 1
        distribuicao_bruta[ano] = dias_no_ano

    resultado_final = {}
    soma_atual = 0
    maior_valor = -1
    ano_maior_valor = -1

    for ano, dias in distribuicao_bruta.items():
        proporcao = round(dias / total_dias, 2)
        resultado_final[ano] = proporcao
        soma_atual += proporcao
        
        if proporcao > maior_valor:
            maior_valor = proporcao
            ano_maior_valor = ano
            
    diferenca = round(1.00 - soma_atual, 2)
    
    if diferenca != 0:
        resultado_final[ano_maior_valor] += diferenca
        resultado_final[ano_maior_valor] = round(resultado_final[ano_maior_valor], 2)

    return resultado_final, None

# --- Interface ---

st.markdown('<p class="main-title">Distribuição Orçamentária</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Calcule a proporção do contrato por ano fiscal</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    dt_inicio = st.date_input("Início da Vigência", value=date.today(), format="DD/MM/YYYY")

with col2:
    dt_fim = st.date_input("Fim da Vigência", value=date.today() + datetime.timedelta(days=365), format="DD/MM/YYYY")

col_vazia_esq, col_btn, col_vazia_dir = st.columns([1, 2, 1])

with col_btn:
    calcular = st.button("Calcular Proporção", use_container_width=True)

# --- Processamento ---

if calcular:
    dados, erro = calcular_distribuicao(dt_inicio, dt_fim)
    
    if erro:
        # Removido indentação para evitar bloco de código
        st.markdown(f'<div class="custom-warning">{erro}</div>', unsafe_allow_html=True)
    else:
        cards_html = ""
        for ano, valor in dados.items():
            percentual = int(valor * 100)
            # A construção da string HTML abaixo está colada à esquerda para evitar indentação indesejada
            cards_html += f"""
<div class="metric-custom metric-year">
    <div class="label">Ano {ano}</div>
    <div class="value">{valor:.2f}</div>
    <div class="details">{percentual}% do orçamento</div>
</div>"""
        
        # O HTML final também está sem indentação na primeira linha
        final_html = f"""
<div class="results-container">
    <div class="section-container">
        <h3>Resultado da Distribuição</h3>
        <p style="font-size: 0.9rem; opacity: 0.8;">Soma total: 1.00</p>
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
