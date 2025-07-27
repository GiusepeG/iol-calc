# -*- coding: utf-8 -*-
# NOME DO ARQUIVO: generate_interactive_chart.py

import pandas as pd
import plotly.graph_objects as go
from typing import List

# --- Configurações ---
INPUT_CSV = 'resultados_consolidados_iol.csv'
OUTPUT_HTML = 'grafico_comparativo_formulas.html'

def create_interactive_chart(df: pd.DataFrame, formula_columns: List[str]):
    """
    Cria e salva um gráfico interativo comparando as fórmulas de LIO com eixos fixos.

    Args:
        df (pd.DataFrame): O DataFrame contendo os dados.
        formula_columns (List[str]): A lista de nomes das colunas das fórmulas a serem plotadas.
    """
    print("Criando o gráfico interativo com eixos fixos...")
    
    # --- Define os limites fixos para os eixos ---
    x_min = df['axial_length'].min()
    x_max = df['axial_length'].max()
    
    # Encontra o valor mínimo e máximo em todas as colunas de fórmula
    y_min = df[formula_columns].min().min()
    y_max = df[formula_columns].max().max()
    
    # Adiciona uma pequena margem de 5% para melhor visualização
    y_range = y_max - y_min
    y_axis_min = y_min - (y_range * 0.05)
    y_axis_max = y_max + (y_range * 0.05)

    fig = go.Figure()

    # --- Adiciona uma linha (trace) para cada fórmula ---
    for formula_name in formula_columns:
        fig.add_trace(
            go.Scatter(
                x=df['axial_length'],
                y=df[formula_name],
                name=formula_name,
                mode='lines+markers'
            )
        )

    # --- Atualiza o layout do gráfico ---
    # A caixa de seleção (updatemenus) foi removida.
    fig.update_layout(
        title_text="Comparativo de Fórmulas de Cálculo de LIO",
        xaxis_title="Comprimento Axial (mm)",
        yaxis_title="Potência da LIO (D)",
        legend_title="Fórmulas",
        xaxis_range=[x_min, x_max],  # Define o eixo X fixo
        yaxis_range=[y_axis_min, y_axis_max]  # Define o eixo Y fixo
    )
    
    # Salva o gráfico em um arquivo HTML
    try:
        fig.write_html(OUTPUT_HTML)
        print(f"\nGráfico interativo salvo com sucesso como '{OUTPUT_HTML}'.")
        print("Abra este arquivo em um navegador para usar a interatividade.")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o arquivo HTML: {e}")


def main():
    """
    Função principal que carrega os dados e inicia a criação do gráfico.
    """
    try:
        df = pd.read_csv(INPUT_CSV)
        print(f"Arquivo '{INPUT_CSV}' carregado com sucesso.")
    except FileNotFoundError:
        print(f"ERRO: O arquivo de entrada '{INPUT_CSV}' não foi encontrado.")
        print("Certifique-se de que ele está na mesma pasta que este script.")
        return

    # Identifica automaticamente as colunas das fórmulas, excluindo as de biometria
    biometry_cols = ['iol_model', 'a_constant', 'eye_side', 'axial_length', 
                     'meas_k1', 'meas_k2', 'optical_acd']
    formula_cols = [col for col in df.columns if col not in biometry_cols]
    
    print(f"Fórmulas encontradas para plotar: {formula_cols}")
    
    # Remove colunas que são totalmente nulas, se houver, para evitar erros de cálculo de min/max
    df.dropna(axis=1, how='all', inplace=True)
    formula_cols = [col for col in formula_cols if col in df.columns]

    create_interactive_chart(df, formula_cols)


if __name__ == "__main__":
    main()
