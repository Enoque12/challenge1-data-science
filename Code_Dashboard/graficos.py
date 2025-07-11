import plotly.express as px
import plotly.graph_objects as go
from utils import formatar_metical
import streamlit as st
import numpy as np
import pandas as pd

def grafico_faturamento(loja, valor, total):
    
    sub1, = st.columns(1)
    
    with sub1:
        st.write('')
    fig = go.Figure(data=[go.Pie(
        labels=[loja, 'Total'],
        values=[valor, total],
        hole=0.6,
        marker=dict(colors=['#00cc96', '#e8e8e8']),
        textinfo='none'
    )])
    fig.update_layout(
        title_text=f'Faturamento da {loja}',
         height=550, 
        annotations=[dict(text=f'{formatar_metical(round(valor,2))}',
        x=0.5, y=0.5,
        font_size=24, 
        showarrow=False)]
    )
    st.plotly_chart(fig, use_container_width=True)

def grafico_vendas_categoria(df):
    
    sub1, sub2 = st.columns(2)
    
    with sub1:
        categoria = st.selectbox('Categoria', df['Categoria do Produto'].unique(), label_visibility="collapsed")
    
    df_categoria = df[df['Categoria do Produto'] == categoria].groupby('Produto')['Preço'].sum().reset_index()
    total = df_categoria['Preço'].sum()
    st.write(f"Total da categoria {categoria}: {formatar_metical(round(total, 2))}")

    fig = px.bar(
        df_categoria,
        x='Produto',
        y='Preço',
        color='Preço',
        color_continuous_scale=["#ccf5e7", "#00cc96", "#007b5e"],
        title='Vendas por Categoria'
    )
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

def grafico_vendas_ano_categoria(df):
    
    sub1, sub2, sub3, sub4 = st.columns(4)
    
    with sub1:
        ano = st.selectbox("Ano", np.int64(np.msort(df['Data da Compra'].dt.year.unique())), key="ano_cat")
    
    df_ano = df[df['Data da Compra'].dt.year == ano]
    df_resumo = df_ano.groupby('Categoria do Produto')['Preço'].sum().reset_index()

    fig = px.bar(
        df_resumo,
        x='Categoria do Produto',
        y='Preço',
        color='Preço',
        color_continuous_scale=["#ccf5e7", "#00cc96", "#007b5e"],
        title=f'Vendas por Categoria no Ano {ano}'
    )
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

def grafico_vendas_mensais(df):
    df['Data da Compra'] = df['Data da Compra'].dt.strftime('%Y-%m')
    df_meses = df.groupby(['Data da Compra','Categoria do Produto', 'Produto'])['Preço'].sum().reset_index()
    
    df_meses['Data da Compra'] = pd.to_datetime(df_meses['Data da Compra'])
    
    sub1, sub2, sub3 = st.columns(3)
    
    with sub1:
        ano = st.selectbox("Ano", np.int64(np.sort(df_meses['Data da Compra'].dt.year.unique())), key="ano_mensal")
        
    with sub2:
        categoria = st.selectbox("Categoria", df['Categoria do Produto'].unique(), key="categoria_mensal")
    
    with sub3:
        produto = st.selectbox("Produto", df[df['Categoria do Produto'] == categoria]['Produto'].unique(), key="produto_mensal")
    

    df_aux = df_meses[df_meses['Data da Compra'].dt.year == ano]
    df_aux = df_aux[df_aux['Categoria do Produto'] == categoria]
    df_aux = df_aux[df_aux['Produto'] == produto]

    df_aux['Mês'] = df_aux['Data da Compra'].dt.month_name()
    df_aux['Mês_Num'] = df_aux['Data da Compra'].dt.month

    df_aux = df_aux.sort_values(by='Mês_Num')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_aux['Mês'],
        y=df_aux['Preço'],
        mode='lines+markers',
        line=dict(color='#00cc96', width=3),
        marker=dict(color='#ccf5e7', size=8),
        name='Mensal'
    ))
    fig.update_layout(title="Vendas Mensais", xaxis_title="Mês", yaxis_title="Preço Total")
    st.plotly_chart(fig, use_container_width=True)

def grafico_frete(loja, lojas, df_filtro):
    frete = {l: 0 for l in lojas}
    frete[loja] = round(df_filtro['Frete'].mean(), 2)
    df_frete = pd.DataFrame({'Loja': list(frete.keys()), 'Frete Médio': list(frete.values())})

    cores = {
        lojas[0]: "#007b5e",
        lojas[1]: "#00cc96",
        lojas[2]: "#ccf5e7",
        lojas[3]: "#99e6cc"
    }

    fig = px.bar(df_frete, x="Loja", y="Frete Médio", color="Loja", color_discrete_map=cores, title=f"Frete Médio da {loja}")
    st.plotly_chart(fig, use_container_width=True)

def grafico_avaliacao(loja, media_loja, media_total):
    percentual = round((media_loja / media_total) * 100, 2)
    fig = go.Figure(data=[go.Pie(
        labels=[loja, 'Total'],
        values=[percentual, 100],
        hole=0.6,
        marker=dict(colors=['#007b5e', '#f2f2f2']),
        textinfo='none'
    )])
    fig.update_layout(
        title_text=f'Avaliação Média da {loja}',
        height=500,
        annotations=[dict(text=f'{percentual}%', x=0.5, y=0.5, font_size=23, showarrow=False)]
    )
    st.plotly_chart(fig, use_container_width=True)
