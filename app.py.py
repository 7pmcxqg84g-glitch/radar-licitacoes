import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import urllib.parse

# Configuração visual profissional
st.set_page_config(page_title="Radar de Licitações CE", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; background-color: #25d366; color: white; border-radius: 10px; }
    .card { background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #003366; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ Radar de Licitações: Assessorias no Ceará")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135706.png", width=100)
st.sidebar.title("Painel de Controle")

# Configurações de Busca
uf = "CE"
termo = st.sidebar.text_input("Buscar por:", "Assessoria Contabil")
zap_numero = "5585981722321"

def buscar_dados():
    # API do PNCP (Portal Nacional de Contratações Públicas)
    url = "https://pncp.gov.br/api/pncp/v1/contratacao/ultimas"
    params = {"pagina": 1, "tamanhoPagina": 30, "uf": uf, "termo": termo}
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json()['data'] if r.status_code == 200 else []
    except:
        return []

data = buscar_dados()

tab1, tab2 = st.tabs(["🔍 Oportunidades Reais", "📅 Minha Agenda Mensal"])

if data:
    agendados = []
    with tab1:
        st.subheader(f"Licitações encontradas no Ceará para: '{termo}'")
        for item in data:
            orgao = item['orgaoEntidade']['razaoSocial']
            objeto = item['objeto']
            data_ab_str = item['dataAberturaProposta']
            dt_obj = datetime.fromisoformat(data_ab_str.split('T')[0])
            data_fmt = dt_obj.strftime('%d/%m/%Y')
            
            link_edital = f"https://pncp.gov.br/app/editais/{item['orgaoEntidade']['cnpj']}/{item['anoContratacao']}/{item['sequencialContratacao']}"
            
            # Formatação de Mensagem WhatsApp
            texto_zap = f"🏛 *NOVA LICITAÇÃO CE*\n\n📍 *Órgão:* {orgao}\n📝 *Objeto:* {objeto}\n📅 *Data:* {data_fmt}\n🔗 *Edital:* {link_edital}"
            link_zap = f"https://wa.me/{zap_numero}?text={urllib.parse.quote(texto_zap)}"

            st.markdown(f"""
            <div class="card">
                <h4>{orgao}</h4>
                <p><strong>Objeto:</strong> {objeto}</p>
                <p>📅 <b>Abertura:</b> {data_fmt}</p>
                <a href="{link_edital}" target="_blank">📄 Ver Edital Completo</a>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"📲 Notificar no WhatsApp", key=item['sequencialContratacao']):
                st.markdown(f'<meta http-equiv="refresh" content="0;URL={link_zap}">', unsafe_allow_html=True)

            agendados.append({"Data": dt_obj, "Órgão": orgao, "Link": link_edital})

    with tab2:
        st.subheader("Planejamento Mensal de Participação")
        df = pd.DataFrame(agendados)
        if not df.empty:
            df = df.sort_values(by="Data")
            df['Data'] = df['Data'].dt.strftime('%d/%m/%Y')
            st.table(df)
        else:
            st.write("Nenhuma licitação encontrada para agendar.")
else:
    st.info("Buscando novas licitações no portal do TCE-CE e PNCP... Se nada aparecer, tente mudar o termo de busca.")

st.sidebar.info("💡 **Dica Profissional:** Verifique os editais com 10 dias de antecedência para organizar as certidões negativas.")