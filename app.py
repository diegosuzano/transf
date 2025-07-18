import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuração da página
st.set_page_config(page_title="Registro Transferência", layout="centered")
st.title("🚚 Registro de Transferência de Carga")

# Autenticação com Google Sheets usando credenciais embutidas
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

credenciais_dict = {
  "type": "service_account",
  "project_id": "novatransferencia",
  "private_key_id": "e0655f862376f9d30f60fa84b94e26cda2ed4263",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC8Yla4VMd6KLDx\n5YWQyoho9ecmQn4aY1o5gtkwirlJ69J8269KpIDWY8MbyhZVEy1DE6FCnwyh0TeN\nh+cNzaemx5GE7J9FI+kEi7fbW87SztZt0xhoqwPHUUknb1IdQJ4SV0hSJoYH1TuE\nThi+fEYp8Dr03dGyvykn3q2NQey+tntcmv8I1eoXaanKOAU+99mltVabhtKcKwmb\nvjms5G9ic9IrhhgKKD/HdX3Xrf37TkI3zz5pUVHf4ZW/BYl0KFaDAhpoo9zF73BT\nrQVC2QqdAP7Aloix+O4CTTDFvjk/UsWE8xws9mm12cCbd5igKC5+52STY4LugA89\n8jQUPK5DAgMBAAECggEAE8lSaXcCIqsOdsHQRxZ2wGt/lU2rmBLyYZMEQ+x2LLT3\nvUSHw1PG8n20+wC9Wr8yZFa1+9zfw0lJx/RLyO/eWY6hkrAVxHnSmjcgnwokDZFL\nBWsEJ846jd9USy+OlOL6F1wSjQpdzonPgASB5dQAvJvuXVTFFzyr0nO5j9oqRxeO\nUXECUyU+KUFalXUHn/Lk93DEqkDCWDvnNOrht/Te2MjCXfavLQGQRNUax6oAcacu\nlXaJ6HEBWzCl3v9yf5pArC+wl25qf49ef5PzL3lk08SZVjH3GkYOsQTKxMhADSmN\nrGR5jQ5wHjtkwBHYfbacMKTKaOR1i0EzM3foib2Y8QKBgQDuQe3XWMLC2gDYDNB9\nXb2wm16n8KJAwKfw6Qd8VERA0L9XgSPlM5qAkoEv1Z1aq5GblgaunUXZB5fNZwHz\nLCDGxAXlI5coWgE0nw5e7D05JnhRb80NE+Wsp+yH6H+KjW2gfCv7HPIpHMk6hjJX\nB33HGXc5Onr+h9AfA3L6zFVnEQKBgQDKaaNTraLmu7UaTinr/0H5M3skvwjFXcyk\nhaLDagvMsmj1Xe/VPc3MD1wLCWsP9Rlp24RXOzEF9N5uJtYj+ZEsngok5sWP643o\ncDD77082oik0lavGeQvWTDVqRSKvKby5jlw1eprK4k+BnyG389pKREidiJdZ/wKO\n+CnyKtWIEwKBgEpQ8jkLjKRuj3jUdmvEQ5jEvb+whUuhTEEOzrDvL+Lvud83ftTN\nRdH44KblAJH5lg9rumXY1KKfhbAiAy+wggC9wAD7GvkRKfMZ8ceV9HrRDxKHxvPf\nUvKJ5nN2B+JVvu4iDS3kl3xPaE0C8szGn2rs/I0zOo4OGtKxprmn5rOhAoGBAJy9\nUsFQew3LGwFkt6fNAQx1Jg2ddLBI41gfN5u0+bAoE4i1lit9cWhsGG1ffK1dsbE8\nUG2wI1Umeju4DSjMb/Op6dcLcL7yu+/bOMNOW/vFdL0IjXzibR0j5FUHdkVHv6G8\nsIClEUq8Fq8cR+MHjOjnmYeLpxAEnbmSSAED1FhLAoGBAJimayf6cx1HOVF8ChO7\nCnVQrxAyizKM3e0Pgdr8h0u0ydUuPXi/Q6VsS4N06iJrlDylNv/zxBZ5uKw7zC27\nTCjYsevh3x2k+K35Pb5deNVmdNuIGRfo6ZAK8TOUkkTNX8KOSITQQP7tC1u1rNhZ\nfq1sFrsUuGuM8IAAwVcAJ7Pu\n-----END PRIVATE KEY-----\n",
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
    if st.button(f"Registrar {label}"):
        st.session_state[label] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# sessão
campos_tempo = [
    "Entrada na Fábrica", "Encostou na doca Fábrica", "Início carregamento", "Fim carregamento",
    "Faturado", "Amarração carga", "Saída do pátio", "Entrada CD", "Encostou na doca CD",
    "Início Descarregamento CD", "Fim Descarregamento CD", "Saída CD"
]

for campo in campos_tempo:
    if campo not in st.session_state:
        st.session_state[campo] = ""

# Campos manuais
st.subheader("Dados do Veículo")
data = st.date_input("Data", value=datetime.today())
placa = st.text_input("Placa do caminhão")
conferente = st.text_input("Nome do conferente")

# Campos com botões
st.subheader("Fábrica")
for campo in campos_tempo[:7]:
    registrar_tempo(campo)
    st.text_input(campo, value=st.session_state[campo], disabled=True)

st.subheader("Centro de Distribuição (CD)")
for campo in campos_tempo[7:]:
    registrar_tempo(campo)
    st.text_input(campo, value=st.session_state[campo], disabled=True)

# Calcular tempos automáticos
def calc_tempo(fim, inicio):
    try:
        t1 = datetime.strptime(st.session_state[fim], "%Y-%m-%d %H:%M:%S")
        t0 = datetime.strptime(st.session_state[inicio], "%Y-%m-%d %H:%M:%S")
        return str(t1 - t0)
    except:
        return ""

tempo_carreg = calc_tempo("Fim carregamento", "Início carregamento")
tempo_espera = calc_tempo("Encostou na doca Fábrica", "Entrada na Fábrica")
tempo_total = calc_t
