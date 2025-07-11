# -*- coding: utf-8 -*-
"""KNN(v3).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yT7zJ5erGoLj0YdCsFE9PdMSBBYKyApy

# Importando e tratando os dados
"""

!pip install kagglehub

import kagglehub

# Download latest version
path = kagglehub.dataset_download("asaniczka/tmdb-movies-dataset-2023-930k-movies")

print("Path to dataset files:", path)

"""Escolha de colunas julgadas como mais importantes para a pipeline"""

import pandas as pd
colunas_escolhidas = ["id", "title", "vote_average", "vote_count", "release_date", "revenue", "runtime", "adult", "budget", "overview", "popularity", "genres", "keywords"]
dados = pd.read_csv(f"{path}/TMDB_movie_dataset_v11.csv", usecols=colunas_escolhidas)

dados = dados.dropna(subset='title')

print(f" Os seus dados estão com a seguinte configuração: {dados.shape}\n")
dados.head(2)

"""Analisar quantidade de nulos presentes nas colunas a serem utilizadas

# Versão 2 KNN

## One-Hot Encoding
"""

generos = dados['genres']
generos.fillna('Desconhecido', inplace=True)
display(generos.head(2))

#OneHot Encoding dos gêneros
genres_dummies = generos.str.get_dummies(sep=', ')
display(genres_dummies.head(2))
print(genres_dummies.shape)

"""Aqui temos a tabela inteira com os gêneros corrigidos pelo one-hot encoding"""

df_final = pd.concat([dados, genres_dummies], axis=1)
display(df_final.head(2))
print(df_final.shape)

#Vamos desconsiderar a data completa e focar apenas no ano de lançamento
df_final['release_date'] = pd.to_datetime(df_final['release_date'])
df_final['release_year'] = df_final['release_date'].dt.year
df_final = df_final.drop('release_date', axis=1)

#Joga filmes com título nulo fora
df_final = df_final.dropna(subset=['title'])

"""## Inputation das datas"""

#Temos alguns anos de lançamento vazios, faremos inputation com a data média
media_ano = df_final['release_year'].mean()
df_final['release_year'] = df_final['release_year'].fillna(value=media_ano)

"""Vamos aplicar o MinMaxScaler para normalizar os dados numéricos para nossso KNN"""

from sklearn.preprocessing import MinMaxScaler

#Aproveitando para arrumar booleano da coluna Adult
df_final['adult'] = df_final['adult'].astype(int)

# 1. Inicialize o scaler
scaler = MinMaxScaler()

# 2. Defina as colunas que você quer escalar
colunas_para_escalar = ['vote_average', 'vote_count', 'release_year', 'revenue', 'runtime', 'budget', 'popularity']

# 3. Use fit_transform nas colunas selecionadas
df_final[colunas_para_escalar] = scaler.fit_transform(df_final[colunas_para_escalar])

print("\nDataFrame com Variáveis Escaladas:")
display(df_final.head(2))

"""## TF-IDF"""

from sklearn.feature_extraction.text import TfidfVectorizer

# 1. Preparar a Coluna 'overview' - Um Passo Crucial
# O TF-IDF não sabe lidar com valores nulos (NaN). Vamos preenchê-los com uma string vazia.
# Supondo que seu DataFrame se chame 'dados'
dados['overview_limpo'] = dados['overview'].fillna('Desconhecido')

# 2. Inicializar o TfidfVectorizer (aqui definimos as regras do jogo)
# stop_words='english': Remove palavras comuns em inglês como 'the', 'a', 'is', que não agregam valor.
# max_features=5000: Limita o nosso vocabulário às 5000 palavras mais frequentes.
# Isso é ESSENCIAL para controlar o uso de memória e focar no que importa.
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)

# 3. Treinar o modelo e transformar as sinopses em uma matriz numérica
# O .fit_transform() aprende o vocabulário e cria a matriz TF-IDF de uma só vez.
overview_tfidf_matrix = tfidf_vectorizer.fit_transform(dados['overview_limpo'])

# 4. Inspecionar o resultado
print("Formato da matriz TF-IDF gerada (filmes, palavras):")
print(overview_tfidf_matrix.shape)

print("\nTipo da matriz gerada:")
print(type(overview_tfidf_matrix))

df_final = df_final.drop(['title', 'overview', 'genres', 'keywords'], axis=1)

df_final.dtypes

from scipy.sparse import hstack, csr_matrix
import numpy as np

# --- 1. Garantir que todas as peças estejam no formato correto ---
# O hstack funciona melhor se todos forem matrizes (esparsas ou densas em formato numpy).
# Vamos pegar apenas os valores do DataFrame de dummies de gênero.
genres_array = genres_dummies.values

# --- 2. Combinar tudo com hstack ---
# O hstack recebe uma tupla de matrizes para empilhar horizontalmente.
# É uma boa prática converter as matrizes densas para o formato esparso antes de juntar.
print("Combinando as matrizes...")

print(f"DF_FINAL => {len(df_final)} \nGenero => {len(genres_array)}")

matriz_final_features = hstack((
    csr_matrix(df_final),
    csr_matrix(genres_array),
    overview_tfidf_matrix
))


# --- 3. Verificar o resultado final ---
print("\n--- Supermatriz de Features Final ---")
print("Formato da matriz final combinada (filmes, features totais):")
print(matriz_final_features.shape)

print("\nTipo da matriz final:")
print(type(matriz_final_features))
print("Pronta para ser usada no modelo KNN!")

"""# KNN de fato"""

from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import pandas as pd

df_numerico = matriz_final_features

"""Treinamento do modelo KNN"""

# --- 2. Escalonamento ---
# Todos os dados precisam estar na mesma escala para o KNN funcionar bem
'''scaler = MinMaxScaler()
features_escalonadas = scaler.fit_transform(df_numerico)

print("\n--- Amostra das Features Escalonadas (Array NumPy) ---")
print(features_escalonadas[:5])'''

# --- 3. Treinamento do Modelo ---
# algorithm='brute' é direto, mas para datasets maiores 'kd_tree' ou 'ball_tree' podem ser mais rápidos
knn_model = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')

# "Treinamos" o modelo com nossos dados escalonados
knn_model.fit(matriz_final_features)

print("\nModelo KNN treinado com sucesso!")

import pandas as pd
from sklearn.neighbors import NearestNeighbors

# --- A Função de Recomendação (CORRIGIDA) ---

# Mudei o nome do parâmetro 'dados_escalonados' para 'matriz_features' para ficar mais claro
def recomendar_filmes(titulo, modelo_knn, matriz_features, mapeamento_indices, dados_filmes):
    """
    Recomenda 5 filmes similares a um filme de entrada.
    """
    try:
        idx_lookup = mapeamento_indices[titulo]
        if isinstance(idx_lookup, pd.Series):
            idx = idx_lookup.iloc[0]
        else:
            idx = idx_lookup
    except KeyError:
        return f"Filme '{titulo}' não encontrado no nosso banco de dados. Tente outro."

    # AQUI ESTÁ A CORREÇÃO PRINCIPAL: Usamos a 'matriz_features' que foi passada
    # O [idx] pega a linha correta, e o [ ] em volta transforma em uma lista 2D,
    # que é o formato que o kneighbors espera.
    # Se a matriz_features for esparsa (como a do TF-IDF), não precisa do .values
    distancias, indices_vizinhos = modelo_knn.kneighbors(matriz_features[idx])

    # Pula o primeiro vizinho (o próprio filme)
    indices_filmes_similares = indices_vizinhos[0][1:]

    # Usa o DataFrame original para obter os títulos
    titulos_recomendados = dados_filmes['title'].iloc[indices_filmes_similares].tolist()

    return titulos_recomendados

# --- Exemplo de Uso (Assumindo que 'tfidf_matrix' é sua matriz TF-IDF) ---

# Supondo que você já tenha:
# knn_model: seu modelo KNN treinado com a tfidf_matrix
# tfidf_matrix: sua matriz gerada pelo TfidfVectorizer
# indices: seu mapeamento de título para índice
# dados: seu DataFrame original com a coluna 'title'

filme_exemplo = 'Fight Club'

# <<-- AQUI ESTÁ A MUDANÇA! Passe a matriz TF-IDF aqui.
# Também passei o DataFrame 'dados' para a função pegar os títulos de lá.
recomendacoes = recomendar_filmes(filme_exemplo, knn_model, matriz_final_features, indices, dados)

print(f"Porque você assistiu '{filme_exemplo}', talvez você goste de:")

if isinstance(recomendacoes, list):
    for i, filme in enumerate(recomendacoes):
        print(f"{i+1}. {filme}")
else:
    print(recomendacoes)