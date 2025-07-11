import pandas as pd

def carregar_dados():
    lojas = ['Loja_1', 'Loja_2', 'Loja_3', 'Loja_4']
    df = {loja: pd.read_csv(f'Dados/{loja.lower()}.csv') for loja in lojas}
    for d in df.values():
        d['Data da Compra'] = pd.to_datetime(d['Data da Compra'], format='%d/%m/%Y')
    return lojas, df

def calcular_faturamento(df_dict, loja):
    total = sum(d['Preço'].sum() for d in df_dict.values())
    loja_faturamento = df_dict[loja]['Preço'].sum()
    return total, loja_faturamento

def calcular_avaliacao(df_dict, loja):
    total = sum(d['Avaliação da compra'].mean() for d in df_dict.values())
    loja_avaliacao = df_dict[loja]['Avaliação da compra'].mean()
    return total, loja_avaliacao

def formatar_metical(valor):
    moeda = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{moeda} MT"
