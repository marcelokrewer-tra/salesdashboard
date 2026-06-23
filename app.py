import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

st.title("📊 Dashboard Interativo de Vendas")
st.write("Faça o upload da sua planilha abaixo para começarmos a análise.")

# Botão de Upload
arquivo = st.file_uploader("Suba a planilha do Excel (.xlsx)", type=["xlsx"])

if arquivo:
    st.write("---")
    # Ajustador de cabeçalho dinâmico
    linha_cabecalho = st.number_input("Se os nomes das colunas estiverem estranhos, ajuste a linha do cabeçalho aqui:", min_value=0, max_value=15, value=1)
    
    # Lendo o arquivo e ignorando as linhas acima do cabeçalho real
    df = pd.read_excel(arquivo, header=linha_cabecalho)
    
    st.success("Arquivo carregado com sucesso! 🎉")
    
    st.write("### 📋 Suas Colunas Reais (Copie e envie para a IA):")
    st.info(str(df.columns.tolist()))
    
    st.write("### 🔍 Prévia dos Dados:")
    st.dataframe(df.head())
