import streamlit as st
from utils import carregar_dados, calcular_faturamento, calcular_avaliacao, formataData
from graficos import (
    grafico_faturamento,
    grafico_vendas_categoria,
    grafico_vendas_ano_categoria,
    grafico_vendas_mensais,
    grafico_frete,
    grafico_avaliacao
)

st.set_page_config(layout="wide")

st.sidebar.markdown("<h1 style='text-align:center;'>Challenge Alura Store</h1><hr>", unsafe_allow_html=True)

st.markdown(
    """
    <div style="text-align: center;">
        <h1>Análise das Lojas do Senhor João</h1>
        <hr>
    </div>
    """,
    unsafe_allow_html=True
)

# Carregando dados
lojas, df_lojas = carregar_dados()
loja = st.sidebar.selectbox("Lojas", lojas)
df_filtro = df_lojas[loja]

# Página
pagina = st.sidebar.radio("Navegação", ["📊 DataFrames", "📈 Dashboard", "💡 Recomendações"])

if pagina == "📊 DataFrames":
    st.title("🏠 Visão Geral")
    st.write("Bem-vindo ao painel geral das Lojas do Senhor João.")
    st.dataframe(formataData(df_filtro))

elif pagina == "📈 Dashboard":
    st.title(f"📈 Análises - {loja}")
    faturamento_total, faturamento_loja = calcular_faturamento(df_lojas, loja)
    avaliacao_total, avaliacao_loja = calcular_avaliacao(df_lojas, loja)

    col1, col2 = st.columns(2)
    with col1:
        grafico_faturamento(loja, faturamento_loja, faturamento_total)
    with col2:
        grafico_vendas_categoria(df_filtro)

    st.markdown("---")
    col3, = st.columns(1)
    with col3:
        grafico_vendas_ano_categoria(df_filtro)
        
        st.markdown(
            """
            <div style="text-align: center;">
                <hr>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        grafico_vendas_mensais(df_filtro)
        
        st.markdown(
            """
            <div style="text-align: center;">
                <hr>
            </div>
            """,
            unsafe_allow_html=True
        )

    col4, = st.columns(1)
    with col4:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            grafico_frete(loja, lojas, df_filtro)
        with col_g2:
            grafico_avaliacao(loja, avaliacao_loja, avaliacao_total)

elif pagina == "💡 Recomendações":
    st.title("💡 Recomendações")
    st.markdown(
        """
        <h2 style="text-align: center;">📄 Recomendação para o Senhor João</h2>

        <table style="width: 100%; border-collapse: collapse;" border="1">
            <thead>
                <tr>
                    <th>Loja</th>
                    <th>Faturamento</th>
                    <th>Vendas por Categoria</th>
                    <th>Média de Avaliação</th>
                    <th>Média de Frete</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Loja 1</td>
                    <td>1.534.509,12 MT</td>
                    <td>Muito Boa</td>
                    <td>3.977</td>
                    <td>34,692 MT</td>
                </tr>
                <tr>
                    <td>Loja 2</td>
                    <td>1.488.459,06 MT</td>
                    <td>Boa</td>
                    <td>4.037</td>
                    <td>33,622 MT</td>
                </tr>
                <tr>
                    <td>Loja 3</td>
                    <td>1.464.025,03 MT</td>
                    <td>Boa</td>
                    <td>4.048</td>
                    <td>33,074 MT</td>
                </tr>
                <tr>
                    <td>Loja 4</td>
                    <td>1.384.497,58 MT</td>
                    <td>Boa</td>
                    <td>3.996</td>
                    <td>31,279 MT</td>
                </tr>
            </tbody>
        </table>

        <br>
        <p>Após a análise dos principais indicadores das quatro lojas - faturamento, vendas por categoria, avaliação média dos clientes e frete médio - foi possível observar os seguintes pontos:</p>

        <ul>
            <li>
                <b>Loja 1</b>: Maior faturamento e vendas, sendo a mais lucrativa no curto prazo. No entanto, possui a pior avaliação dos clientes e o frete mais elevado. Requer melhorias logísticas e de atendimento.
            </li>
            <li>
                <b>Loja 4</b>: Menor faturamento, avaliações medianas e o menor frete. Apesar do custo logístico vantajoso, apresenta desempenho financeiro inferior.
            </li>
            <li>
                <b>Lojas 2 e 3</b>: Situação intermediária, com bons níveis de avaliação, frete razoável e faturamento próximo da média.
            </li>
        </ul>

        <p><b>📌 Recomendação:</b><br>
        Para o Sr. João, a melhor decisão neste momento seria <b>vender a Loja 4</b>, visto que ela possui o menor retorno financeiro e não se destaca nos demais indicadores.<br>
        A <b>Loja 1</b> deve ser mantida e priorizada para ações de melhoria, como renegociação de frete e investimento na experiência do cliente, pois é a que demonstra maior potencial de lucro a longo prazo.
        </p>
        """,
        unsafe_allow_html=True
    )

st.markdown("<hr><div style='text-align:center; color:gray;'><small>Desenvolvido por Enoque Mandlate © 2025</small></div>", unsafe_allow_html=True)
