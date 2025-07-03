# server.py
from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import warnings

# Ignorar avisos não críticos
warnings.simplefilter(action='ignore', category=FutureWarning)

# --- INÍCIO DA LÓGICA DO SEU SCRIPT KNN ---

def carregar_e_preparar_dados():
    """Carrega, processa os dados e treina o modelo uma única vez."""
    print("1. Carregando e preparando dados...")
    try:
        colunas = ["id", "title", "vote_average", "vote_count", "release_date", "revenue", "runtime", "adult", "budget", "popularity", "genres"]
        df = pd.read_csv("TMDB_movie_dataset_v11.csv", usecols=colunas)
    except FileNotFoundError:
        print("ERRO: TMDB_movie_dataset_v11.csv não encontrado.")
        return None, None, None

    # Garante que o ID seja numérico para a busca
    df['id'] = pd.to_numeric(df['id'], errors='coerce')
    df.dropna(subset=['title', 'id'], inplace=True)
    df['id'] = df['id'].astype(int)
    df.reset_index(drop=True, inplace=True)

    df_processado = df.copy()
    df_processado['genres'].fillna('Desconhecido', inplace=True)
    genres_dummies = df_processado['genres'].str.get_dummies(sep=', ')
    
    df_processado['release_date'] = pd.to_datetime(df_processado['release_date'], errors='coerce')
    df_processado['release_year'] = df_processado['release_date'].dt.year
    df_processado['release_year'].fillna(df_processado['release_year'].mean(), inplace=True)

    df_final = pd.concat([df_processado, genres_dummies], axis=1)
    df_final['adult'] = df_final['adult'].astype(int)

    colunas_numericas = ['vote_average', 'vote_count', 'release_year', 'revenue', 'runtime', 'budget', 'popularity']
    colunas_modelo = colunas_numericas + list(genres_dummies.columns) + ['adult']
    matriz_features = df_final[colunas_modelo].fillna(0)

    scaler = MinMaxScaler()
    features_escalonadas = scaler.fit_transform(matriz_features)

    print("2. Treinando modelo KNN...")
    modelo_knn = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
    modelo_knn.fit(features_escalonadas)
    print("Modelo treinado e pronto!")

    return modelo_knn, df_final, features_escalonadas

# Carrega tudo na inicialização do servidor
modelo, dados, matriz = carregar_e_preparar_dados()

def obter_recomendacoes_por_id(movie_id):
    """Função que usa o ID do filme para gerar recomendações."""
    # Encontra o índice do dataframe correspondente ao ID do filme
    idx_series = dados.index[dados['id'] == movie_id]
    
    if idx_series.empty:
        print(f"ID {movie_id} não encontrado no dataset.")
        return []

    idx = idx_series[0]

    distancias, indices = modelo.kneighbors([matriz[idx]])
    indices_similares = indices[0][1:]
    titulos_recomendados = dados['title'].iloc[indices_similares].tolist()
    return titulos_recomendados

# --- FIM DA LÓGICA DO KNN ---


# --- CONFIGURAÇÃO DO SERVIDOR FLASK ---
app = Flask(__name__)
CORS(app) # Permite que o React (em outra porta) acesse esta API

# A rota agora espera um ID de filme (inteiro)
@app.route('/recommend/<int:movie_id>')
def recommend(movie_id):
    print(f"Recebida requisição para o ID: {movie_id}")
    recomendacoes = obter_recomendacoes_por_id(movie_id)
    return jsonify(recomendacoes)

if __name__ == '__main__':
    print("Iniciando servidor Flask na porta 5000...")
    app.run(port=5000)
