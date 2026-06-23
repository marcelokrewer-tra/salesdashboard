import streamlit as st
import pandas as pd

st.title("📊 Meu Dashboard de Vendas")
st.write("Bem-vindo ao sistema de análise. Faça o upload da sua planilha abaixo.")

# Botão de Upload
arquivo = st.file_uploader("Suba a planilha do Excel", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)
    st.success("Arquivo carregado com sucesso!")
    st.write("### Prévia dos Dados:")
    st.dataframe(df.head()) # Mostra as 5 primeiras linhas
