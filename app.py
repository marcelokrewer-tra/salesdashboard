import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

st.title("📊 Dashboard Interativo de Vendas")
st.write("Faça o upload da sua planilha abaixo para começarmos a análise.")

# Botão de Upload
arquivo = st.file_uploader("Suba a planilha do Excel (.xlsx)", type=["xlsx"])

if arquivo:
    # Lendo o arquivo
    df = pd.read_excel(arquivo)
    st.success("Arquivo carregado com sucesso! 🎉")
    
    st.write("---")
    st.write("### 📋 Suas Colunas (Copie e envie para a IA):")
    st.info(str(df.columns.tolist()))
    
    st.write("### 🔍 Prévia dos Dados:")
    st.dataframe(df.head())
