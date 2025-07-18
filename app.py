import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuração da página
st.set_page_config(page_title="Registro Transferência", layout="centered")
st.title("🚚 Registro de Transferência de Carga")

# Autenticação com Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

credenciais_dict = {
    "type": "service_account",
    "project_id": "novatransferencia",
    "private_key_id": "e0655f862376f9d30f60fa84b94e26cda2ed4263",
    "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC8Yla4VMd6KLDx\\n...\\n-----END PRIVATE KEY-----\\n",
    "client_email": "novatransferencia@novatransferencia.iam.gserviceaccount.com",
    "client_id": "114919807716623426202",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/novatransferencia%40novatransferencia.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

creds = ServiceAccountCredentials.from_json_keyfile_dict(credenciais_dict, scope)
client = gspread.authorize(creds)

# ID da planilha e nome da aba
SHEET_ID = "1wlPpdjqAXwLfrYqnOp1AE9Ez_gTrcYcT3AD9VB6sMAY"
SHEET_NAME = "Página1"
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# Função para registrar timestamp atual
def registrar_tempo(label):
    if st.button(f"pos_tempo = [
    "Entrada na Fábrica", "Encostou na doca Fábrica", "Início carregamento", "Fim carregamento",
    "Faturado", "Amarração carga", "Saída do pátio", "Entrada CD", "Encostou na doca CD",
    "Início Descarregamento CD", "Fim Descarregamento CD", "Saída CD"
]

for campo in campos_tempo:
    if campo not in st.session_state:
        st.session_state[campo] = ""

st.subheader("Dados do Veículo")
data = st.date_input("Data", value=datetime.today())
placa = st.text_input("Placa do caminhão")
conferente = st.text_input("Nome do conferente")

st.subheader("Fábrica")
for campo in campos_tempo[:7]:
    registrar_tempo(campo)
    st.text_input(campo, value=st.session_state[campo], disabled=True)

st.subheader("Centro de Distribuição (CD)")
for campo in campos_tempo[7:]:
    registrar_tempo(campo)
    st.text_input(campo, value=st.session_state[campo], disabled=True)

def calc_tempo(fim, inicio):
    try:
        t1 = datetime.strptime(st.session_state[fim], "%Y-%m-%d %H:%M:%S")
        t0 = datetime.strptime(st.session_state[inicio], "%Y-%m-%d %H:%M:%S")
        return str(t1 - t0)
    except:
        return ""

tempo_carreg = calc_tempo("Fim carregamento", "Início carregamento")
tempo_espera = calc_tempo("Encostou na doca Fábrica", "Entrada na Fábrica")
tempo_total = calc_tempo("Saída do pátio", "Entrada na Fábrica")
tempo_descarga = calc_tempo("Fim Descarregamento CD", "Início Descarregamento CD")
tempo_espera_cd = calc_tempo("Encostou na doca CD", "Entrada CD")
tempo_total_cd = calc_tempo("Saída CD", "Entrada CD")
tempo_percurso = calc_tempo("Entrada CD", "Saída do pátio")

if st.button("✅ Salvar Registro"):
    nova_linha = [
        str(data), placa, conferente,
        *[st.session_state[campo] for campo in campos_tempo],
        tempo_carreg, tempo_espera, tempo_total,
        tempo_descarga, tempo_espera_cd, tempo_total_cd, tempo_percurso
    ]

    sheet.append_row(nova_linha)
    st.success("Registro salvo com sucesso!")

    for campo in campos_tempo:
        st.session_state[campo] = ""

