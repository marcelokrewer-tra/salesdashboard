import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para aproveitar toda a largura da tela
st.set_page_config(page_title="Dashboard Comercial de Vendas", layout="wide")

# Título Principal
st.title("📊 Painel Interativo de Performance de Vendas")
st.markdown("Alimente o sistema com a planilha mensal para atualizar os indicadores automaticamente.")

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("📥 Configurações e Filtros")

# Upload do Arquivo
arquivo = st.sidebar.file_uploader("1. Suba a planilha do Excel (.xlsx)", type=["xlsx"])

# Ajuste de cabeçalho (caso mude a estrutura da planilha)
linha_cabecalho = st.sidebar.number_input("Linha do cabeçalho no Excel:", min_value=0, max_value=15, value=1)

if arquivo:
    # Lendo os dados
    df = pd.read_excel(arquivo, header=linha_cabecalho)
    
    # Tratamento rápido de dados para garantir que tudo que é número seja lido como número
    colunas_numericas = ['QUOTA TOTAL', 'FATURADO TOTAL', 'DEFASAGEM', 'VALOR DE VENDA TOTAL', 'FATURADO E PENDENTE']
    for col in colunas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Filtro por Coordenador
    if 'NOME COORDENADOR' in df.columns:
        lista_coord = ["Todos"] + sorted(df['NOME COORDENADOR'].dropna().unique().tolist())
        coord_selecionado = st.sidebar.selectbox("2. Filtrar por Coordenador", lista_coord)
        if coord_selecionado != "Todos":
            df = df[df['NOME COORDENADOR'] == coord_selecionado]

    # Filtro por Grupo de Produtos
    if 'NOME GRUPO' in df.columns:
        lista_grupo = ["Todos"] + sorted(df['NOME GRUPO'].dropna().unique().tolist())
        grupo_selecionado = st.sidebar.selectbox("3. Filtrar por Grupo de Produto", lista_grupo)
        if grupo_selecionado != "Todos":
            df = df[df['NOME GRUPO'] == grupo_selecionado]

    # --- CORPO PRINCIPAL DO DASHBOARD ---
    
    # 1. BLOCO DE MÉTRICAS (KPIs)
    st.subheader("📌 Indicadores Gerais do Período")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    total_faturado = df['FATURADO TOTAL'].sum()
    total_quota = df['QUOTA TOTAL'].sum()
    total_defasagem = df['DEFASAGEM'].sum()
    
    # Cálculo de atingimento geral
    atingimento_geral = (total_faturado / total_quota * 100) if total_quota > 0 else 0
    
    with kpi1:
        st.metric(label="💰 Total Faturado", value=f"R$ {total_faturado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with kpi2:
        st.metric(label="🎯 Quota Total (Meta)", value=f"R$ {total_quota:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with kpi3:
        st.metric(label="📈 % Atingimento da Meta", value=f"{atingimento_geral:.2f}%")
    with kpi4:
        # Cor vermelha/alerta se houver defasagem acumulada expressiva
        st.metric(label="📉 Defasagem Acumulada", value=f"R$ {total_defasagem:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), delta=f"-{total_defasagem:,.2f}", delta_color="inverse")

    st.write("---")

    # Criando abas para organizar o visual do site
    aba_vendedores, aba_produtos, aba_defasagem = st.tabs(["👥 Ranking Representantes", "📦 Linhas e Grupos", "⚠️ Análise de Defasagem"])

    # ABA 1: RANKING DE VENDEDORES
    with aba_vendedores:
        st.subheader("Top Representantes por Faturamento")
        if 'NOME REPRESENTANTE' in df.columns:
            # Agrupando faturamento por representante
            ranking_rep = df.groupby('NOME REPRESENTANTE')['FATURADO TOTAL'].sum().reset_index()
            ranking_rep = ranking_rep.sort_values(by='FATURADO TOTAL', ascending=False).head(15) # Top 15
            
            # Gráfico Interativo
            fig_rep = px.bar(
                ranking_rep, 
                x='FATURADO TOTAL', 
                y='NOME REPRESENTANTE', 
                orientation='h',
                title="Top 15 Representantes que Mais Faturaram",
                labels={'FATURADO TOTAL': 'Total Faturado (R$)', 'NOME REPRESENTANTE': 'Representante'},
                color='FATURADO TOTAL',
                color_continuous_scale='Blues'
            )
            fig_rep.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_rep, use_container_width=True)
            
            # Tabela de suporte
            st.write("### Detalhes dos Representantes Filtrados")
            tabela_rep = df.groupby('NOME REPRESENTANTE')[['QUOTA TOTAL', 'FATURADO TOTAL', 'DEFASAGEM']].sum()
            tabela_rep['% ATINGIMENTO'] = (tabela_rep['FATURADO TOTAL'] / tabela_rep['QUOTA TOTAL'] * 100).round(2)
            st.dataframe(tabela_rep.sort_values(by='FATURADO TOTAL', ascending=False), use_container_width=True)

    # ABA 2: PRODUTOS / GRUPOS
    with aba_produtos:
        st.subheader("Análise por Grupos e Linhas de Produtos")
        col_esq, col_dir = st.columns(2)
        
        with col_esq:
            if 'NOME GRUPO' in df.columns:
                vendas_grupo = df.groupby('NOME GRUPO')['FATURADO TOTAL'].sum().reset_index()
                fig_grupo = px.pie(vendas_grupo, values='FATURADO TOTAL', names='NOME GRUPO', title="Faturamento por Grupo de Produto", hole=0.4)
                st.plotly_chart(fig_grupo, use_container_width=True)
                
        with col_dir:
            if 'LINHA' in df.columns:
                vendas_linha = df.groupby('LINHA')['FATURADO TOTAL'].sum().reset_index().sort_values(by='FATURADO TOTAL', ascending=False)
                fig_linha = px.bar(vendas_linha, x='LINHA', y='FATURADO TOTAL', title="Faturamento por Linha", color='FATURADO TOTAL')
                st.plotly_chart(fig_linha, use_container_width=True)

    # ABA 3: DEFASAGEM
    with aba_defasagem:
        st.subheader("Onde estão os maiores gargalos de meta? (Defasagem)")
        
        if 'NOME REPRESENTANTE' in df.columns:
            # Maiores defasagens
            defasa_rep = df.groupby('NOME REPRESENTANTE')['DEFASAGEM'].sum().reset_index()
            defasa_rep = defasa_rep.sort_values(by='DEFASAGEM', ascending=False).head(10) # Maiores problemas
            
            fig_defasa = px.bar(
                defasa_rep,
                x='NOME REPRESENTANTE',
                y='DEFASAGEM',
                title="Top 10 Maiores Defasagens por Representante (Falta para bater a meta)",
                labels={'DEFASAGEM': 'Valor de Defasagem (R$)', 'NOME REPRESENTANTE': 'Representante'},
                color='DEFASAGEM',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig_defasa, use_container_width=True)
            
            st.warning("💡 **Dica de Ação:** Os representantes listados acima são os que estão mais distantes de cumprir suas respectivas quotas no filtro selecionado.")

else:
    st.info("💡 Por favor, faça o upload do arquivo Excel na barra lateral esquerda para visualizar o dashboard.")
