import streamlit as st
import datetime
from datetime import date
import streamlit.components.v1 as components
import re
import calendar

# --- Configuração da Página ---
st.set_page_config(page_title="Calculadora de Orçamento", page_icon="💰", layout="centered")

# --- CSS / Identidade Visual OTIMIZADA ---
page_bg_img = """
<style>
/* Fundo Geral */
[data-testid="stApp"] {
    background-image: linear-gradient(rgb(2, 45, 44) 0%, rgb(0, 21, 21) 100%);
    background-attachment: fixed;
}

/* Limpeza da Interface Base */
[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
[data-testid="stStatusWidget"] {display:none;}

/* Tipografia Geral */
.stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label, span, div {
    color: #e0e0e0 !important;
}

/* Container Principal */
.main .block-container { 
    max-width: 800px; 
    padding-bottom: 5rem;
}

.main-title { font-size: 2.2rem !important; font-weight: bold; text-align: center; }
.sub-title { color: gray; text-align: center; font-size: 1.25rem !important; margin-bottom: 2rem; }

/* =========================================
   NOVA ESTILIZAÇÃO DOS INPUTS (CLEAN E ESTÁVEL)
   ========================================= */

/* 1. Limpa os fundos e bordas padrão das camadas externas do Streamlit */
div[data-testid="stTextInput"] > div:first-child,
div[data-testid="stDateInput"] > div:first-child,
div[data-testid="stSelectbox"] > div:first-child,
div[data-testid="stNumberInput"] > div:first-child {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* 2. Estiliza a caixa real onde digitamos (base-input e o container do select) */
.stTextInput div[data-baseweb="base-input"],
.stDateInput div[data-baseweb="base-input"],
.stNumberInput div[data-baseweb="base-input"],
.stSelectbox div[data-baseweb="select"] > div:first-child {
    background-color: rgba(0, 0, 0, 0.4) !important; /* Fundo escuro levemente transparente */
    border-radius: 16px !important; /* Bordas arredondadas e modernas (sem quebrar layout) */
    border: 1px solid rgba(255, 255, 255, 0.05) !important; /* Borda quase invisível para estabilizar */
    padding: 6px 15px !important; /* Dá o volume natural da caixa sem forçar 'height' */
    transition: all 0.2s ease-in-out;
}

/* 3. Textos dentro dos inputs de texto, data e número */
input[type="text"], input[type="number"] {
    color: #ffffff !important;
    text-align: center !important; /* Centraliza perfeitamente */
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    -webkit-text-fill-color: #ffffff !important; /* Força cor no Chrome/Safari */
    background-color: transparent !important;
}

/* 4. Textos dentro do Selectbox (Dropdown) */
div[data-baseweb="select"] [class*="ValueContainer"] {
    justify-content: center !important; /* Centraliza via flexbox nativo */
    padding: 0 !important;
}
div[data-baseweb="select"] [class*="singleValue"] {
    color: #ffffff !important;
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    text-align: center !important;
}

/* Cor da setinha do Selectbox */
div[data-baseweb="select"] svg {
    fill: #dd4f05 !important;
}

/* 5. Interações suaves (Hover e Focus) */
.stTextInput div[data-baseweb="base-input"]:hover,
.stDateInput div[data-baseweb="base-input"]:hover,
.stNumberInput div[data-baseweb="base-input"]:hover,
.stSelectbox div[data-baseweb="select"] > div:first-child:hover {
    border-color: rgba(221, 79, 5, 0.4) !important; /* Borda fica laranja sutil ao passar o mouse */
    background-color: rgba(0, 0, 0, 0.6) !important;
}

.stTextInput div[data-baseweb="base-input"]:focus-within,
.stDateInput div[data-baseweb="base-input"]:focus-within,
.stNumberInput div[data-baseweb="base-input"]:focus-within,
.stSelectbox div[data-baseweb="select"] > div:first-child:focus-within {
    border-color: #dd4f05 !important; /* Borda laranja forte ao clicar */
    box-shadow: 0 0 8px rgba(221, 79, 5, 0.3) !important; /* Brilho leve */
}

/* Labels Centralizadas acima dos inputs */
.main div[data-testid="stDateInput"] > label, 
.main div[data-testid="stTextInput"] > label,
.main div[data-testid="stSelectbox"] > label,
.main div[data-testid="stNumberInput"] > label { 
    text-align: center !important; 
    width: 100%; 
    display: block;
    margin-bottom: 8px;
    font-size: 0.95rem;
}

/* Ocultar ícones de interrogação/ajuda */
div[data-testid="InputInstructions"] { display: none; }


/* =========================================
   BOTÕES E CARDS DE RESULTADO
   ========================================= */

/* Botões com efeito NEON */
div[data-testid="stButton"] > button { 
    background-color: rgb(221, 79, 5) !important; 
    color: #FFFFFF !important; 
    border-radius: 4rem; 
    border-color: transparent;
    transition: all 0.3s ease; 
    font-weight: bold;
    padding: 0.75rem 2rem !important; /* Volume usando padding */
    font-size: 1.1rem !important;
    margin-top: 10px;
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

/* Texto dos cards */
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

def parse_valor_brasileiro(valor_str):
    try:
        limpo = valor_str.strip()
        limpo = limpo.replace(".", "")
        limpo = limpo.replace(",", ".")
        return float(limpo)
    except:
        return None

def adicionar_meses(data_origem, meses):
    """Adiciona um número de meses a uma data considerando virada de ano e dias limite."""
    mes_novo = data_origem.month - 1 + meses
    ano_novo = data_origem.year + mes_novo // 12
    mes_novo = mes_novo % 12 + 1
    dia_novo = min(data_origem.day, calendar.monthrange(ano_novo, mes_novo)[1])
    return date(ano_novo, mes_novo, dia_novo)

def calcular_distribuicao_financeira(inicio, fim, valor_total):
    if inicio > fim:
        return None, None, "A data de início deve ser anterior ou igual à data de fim."
    
    total_dias = (fim - inicio).days + 1
    
    ano_inicial = inicio.year
    ano_final = fim.year
    
    distribuicao_dias = {}
    for ano in range(ano_inicial, ano_final + 1):
        inicio_periodo = max(inicio, date(ano, 1, 1))
        fim_periodo = min(fim, date(ano, 12, 31))
        dias_no_ano = (fim_periodo - inicio_periodo).days + 1
        distribuicao_dias[ano] = dias_no_ano

    proporcoes_finais = {}
    soma_proporcoes = 0.0
    ano_maior_dias = -1
    maior_dias = -1

    for ano, dias in distribuicao_dias.items():
        prop = round(dias / total_dias, 2)
        proporcoes_finais[ano] = prop
        soma_proporcoes += prop
        
        if dias > maior_dias:
            maior_dias = dias
            ano_maior_dias = ano
            
    diferenca_prop = round(1.00 - soma_proporcoes, 2)
    if diferenca_prop != 0:
        proporcoes_finais[ano_maior_dias] += diferenca_prop
        proporcoes_finais[ano_maior_dias] = round(proporcoes_finais[ano_maior_dias], 2)

    valores_finais = {}
    soma_valores = 0.0
    
    for ano, prop in proporcoes_finais.items():
        val = round(prop * valor_total, 2)
        valores_finais[ano] = val
        soma_valores += val
        
    diferenca_valor = round(valor_total - soma_valores, 2)
    if diferenca_valor != 0:
        valores_finais[ano_maior_dias] += diferenca_valor
        valores_finais[ano_maior_dias] = round(valores_finais[ano_maior_dias], 2)

    return valores_finais, proporcoes_finais, None

# --- Interface ---

st.markdown('<p class="main-title">Distribuição Orçamentária</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Calcule os valores anuais pela proporção fixa</p>', unsafe_allow_html=True)

# Input de Valor
valor_texto = st.text_input("Valor da Compra (R$)", value="10.000,00")

col1, col2 = st.columns(2)

with col1:
    dt_inicio = st.date_input("Início da Vigência", value=date.today(), format="DD/MM/YYYY")

with col2:
    opcoes_meses = ["12", "24", "30", "36", "60", "Personalizado"]
    escolha = st.selectbox("Duração (Meses)", opcoes_meses, index=0)
    
    if escolha == "Personalizado":
        meses_duracao = st.number_input("Digite a quantidade de meses", min_value=1, value=12, step=1)
    else:
        meses_duracao = int(escolha)

# Calcula a data de fim automaticamente baseado no número de meses (-1 dia de carência comum em contratos)
dt_fim_calculada = adicionar_meses(dt_inicio, meses_duracao) - datetime.timedelta(days=1)

# Mostra uma dica visual sutil de até quando o contrato vai
st.markdown(f"<p style='text-align: center; font-size: 0.85rem; color: #7f8c8d; margin-top: -10px;'>O cálculo será feito até: {dt_fim_calculada.strftime('%d/%m/%Y')}</p>", unsafe_allow_html=True)

col_vazia_esq, col_btn, col_vazia_dir = st.columns([1, 2, 1])

with col_btn:
    calcular = st.button("Calcular Valores", use_container_width=True)

# --- Processamento ---

if calcular:
    valor_valido = True
    valor_float = 0.0
    msg_erro = ""

    if not re.match(r'^[\d\.]+(?:,\d{1,2})?$', valor_texto.strip()):
         valor_valido = False
         msg_erro = "Formato inválido. Use pontos para milhar e vírgula para decimais (ex: 10.000,00)"
    else:
        valor_float = parse_valor_brasileiro(valor_texto)
        if valor_float is None:
            valor_valido = False
            msg_erro = "Erro ao converter valor."

    if not valor_valido:
        st.markdown(f'<div class="custom-warning">{msg_erro}</div>', unsafe_allow_html=True)
    else:
        # Usa a data de fim que foi calculada automaticamente em vez da digitada pelo usuário
        valores, proporcoes, erro_calc = calcular_distribuicao_financeira(dt_inicio, dt_fim_calculada, valor_float)
        
        if erro_calc:
            st.markdown(f'<div class="custom-warning">{erro_calc}</div>', unsafe_allow_html=True)
        else:
            cards_html = ""
            for ano in valores.keys():
                val = valores[ano]
                prop = proporcoes[ano]
                
                valor_formatado = formatar_moeda(val)
                fator_str = f"{prop:.2f}"
                
                cards_html += f"""
<div class="metric-custom metric-year">
    <div class="label">Ano {ano}</div>
    <div class="value">{valor_formatado}</div>
    <div class="details">Fator: {fator_str}</div>
</div>"""
            
            valor_total_fmt = formatar_moeda(valor_float)
            
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
