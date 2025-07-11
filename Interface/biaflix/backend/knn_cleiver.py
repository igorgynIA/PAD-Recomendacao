# -*- coding: utf-8 -*-
"""knn_cleiver.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1c8NZAZHVQ8upQp_XDiK5eysQ9X3u76j1
"""

# recomendar_v2_final.py

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import sys
import warnings

# Ignorar avisos futuros do pandas que não são críticos
warnings.simplefilter(action='ignore', category=FutureWarning)

def carregar_dados(caminho_csv):
    """Carrega o dataset a partir de um caminho local."""
    print("1. Carregando dados...")
    try:
        colunas_escolhidas = ["id", "title", "vote_average", "vote_count", "release_date", "revenue", "runtime", "adult", "budget", "popularity", "genres"]
        df = pd.read_csv(caminho_csv, usecols=colunas_escolhidas)
        return df
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{caminho_csv}' não encontrado. Verifique se ele está na mesma pasta que o script.")
        sys.exit(1)

def preparar_pipeline_completa(df):
    """Executa todo o pipeline de pré-processamento de dados."""
    print("2. Iniciando pré-processamento dos dados...")

    # --- Limpeza Inicial ---
    # Passo crucial: remover filmes sem título primeiro para evitar problemas de alinhamento
    df.dropna(subset=['title'], inplace=True)
    df.reset_index(drop=True, inplace=True) # Resetar o índice após dropar linhas

    # --- Engenharia de Features de Gênero ---
    df['genres'].fillna('Desconhecido', inplace=True)
    genres_dummies = df['genres'].str.get_dummies(sep=', ')

    # --- Engenharia de Features de Data ---
    # Usamos .copy() para evitar o SettingWithCopyWarning
    df_processado = df.copy()
    df_processado['release_date'] = pd.to_datetime(df_processado['release_date'], errors='coerce')
    df_processado['release_year'] = df_processado['release_date'].dt.year
    # Inputação da média para anos nulos
    media_ano = df_processado['release_year'].mean()
    df_processado['release_year'].fillna(value=media_ano, inplace=True)

    # --- Preparação da Matriz Final para o Modelo ---
    # Juntamos os dummies de gênero ao nosso dataframe processado
    df_final_com_features = pd.concat([df_processado, genres_dummies], axis=1)

    # Selecionar todas as colunas que o modelo usará
    colunas_numericas = ['vote_average', 'vote_count', 'release_year', 'revenue', 'runtime', 'budget', 'popularity']
    colunas_generos = list(genres_dummies.columns)
    colunas_para_modelo = colunas_numericas + colunas_generos + ['adult']

    # Converter 'adult' para int
    df_final_com_features['adult'] = df_final_com_features['adult'].astype(int)

    # Criar a matriz final, preenchendo qualquer NaN restante (ex: de budget, revenue) com 0
    matriz_features = df_final_com_features[colunas_para_modelo].fillna(0)

    # --- Escalonamento (aplicado uma única vez) ---
    print("3. Escalonando features...")
    scaler = MinMaxScaler()
    features_escalonadas = scaler.fit_transform(matriz_features)

    # Retornamos a matriz pronta para o modelo e o DF com os títulos para a busca
    return features_escalonadas, df_final_com_features

def treinar_modelo_knn(matriz_features):
    """Treina o modelo NearestNeighbors."""
    print("4. Treinando modelo KNN...")
    modelo_knn = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
    modelo_knn.fit(matriz_features)
    print("Modelo treinado com sucesso!")
    return modelo_knn

def recomendar_filmes(titulo, modelo_knn, dados_processados, matriz_features):
    """Busca um filme e retorna 5 recomendações."""
    # Criamos o mapa de títulos para índices a partir do DF já limpo e alinhado
    indices_map = pd.Series(dados_processados.index, index=dados_processados['title'])

    # Lida com títulos duplicados, pegando o primeiro que encontrar
    if titulo in indices_map and isinstance(indices_map[titulo], pd.Series):
        # Se o título for duplicado, pega o primeiro índice
        idx = indices_map[titulo].iloc[0]
    elif titulo in indices_map:
        # Se for único, pega o índice
        idx = indices_map[titulo]
    else:
        return f"ERRO: Filme '{titulo}' não encontrado no nosso banco de dados."

    distancias, indices_vizinhos = modelo_knn.kneighbors([matriz_features[idx]])
    indices_filmes_similares = indices_vizinhos[0][1:]
    titulos_recomendados = dados_processados['title'].iloc[indices_filmes_similares].tolist()
    return titulos_recomendados

# --- Bloco Principal de Execução ---
if __name__ == "__main__":
    # Nome do arquivo CSV esperado na mesma pasta
    ARQUIVO_CSV = "TMDB_movie_dataset_v11.csv"

    if len(sys.argv) < 2:
        print("\nErro: Por favor, forneça um título de filme entre aspas.")
        print("Exemplo de uso: python recomendar_v2_final.py \"Fight Club\"")
        sys.exit(1)

    titulo_do_filme = sys.argv[1]

    # Executa o pipeline completo
    dados_brutos = carregar_dados(ARQUIVO_CSV)
    matriz_final, df_processado = preparar_pipeline_completa(dados_brutos)
    modelo_treinado = treinar_modelo_knn(matriz_final)

    # Gera e imprime a recomendação
    print("5. Gerando recomendações...")
    recomendacoes = recomendar_filmes(titulo_do_filme, modelo_treinado, df_processado, matriz_final)

    print("-" * 40)
    if isinstance(recomendacoes, list):
        print(f"Porque você assistiu '{titulo_do_filme}', talvez você goste de:")
        for i, filme in enumerate(recomendacoes):
            print(f"{i+1}. {filme}")
    else:
        print(recomendacoes)
    print("-" * 40)