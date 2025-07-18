
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Autenticação com Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credenciais_dict = {
    "type": "service_account",
    "project_id": "seu-projeto-id",
    "private_key_id": "sua-private-key-id",
    "private_key": "-----BEGIN PRIVATE KEY-----\\nSUA\\nCHAVE\\nAQUI\\n-----END PRIVATE KEY-----\\n",
    "client_email": "seu-email@seu-projeto.iam.gserviceaccount.com",
    "client_id": "seu-client-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/seu-email%40seu-projeto.iam.gserviceaccount.com"
}
credenciais = ServiceAccountCredentials.from_json_keyfile_dict(credenciais_dict, scope)
cliente = gspread.authorize(credenciais)

# Nome da planilha
nome_planilha = "NomeDaSuaPlanilha"
planilha = cliente.open(nome_planilha).sheet1

# Função para carregar dados
def carregar_dados():
    dados = planilha.get_all_records()
    return pd.DataFrame(dados)

# Interface Streamlit
st.title("Visualizador de Dados do Google Sheets")
if st.button("Carregar dados"):
    df = carregar_dados()
    st.dataframe(df)
