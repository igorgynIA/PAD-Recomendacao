import axios from 'axios';

// Pega a chave da API do arquivo .env
const API_KEY = import.meta.env.VITE_API_KEY;
const API_BASE_URL = 'https://api.themoviedb.org/3';

// Cria uma instância do axios com a URL base
const client = axios.create({
    baseURL: API_BASE_URL,
    params: { api_key: API_KEY, language: 'pt-BR' }
});

// Função para buscar os filmes de diferentes categorias
export const fetchMovies = async (endpoint) => {
    try {
        const response = await client.get(endpoint);
        return response.data.results;
    } catch (error) {
        console.error("Erro ao buscar filmes:", error);
        return [];
    }
};

// Função para buscar detalhes de um filme específico
export const getMovieDetails = async (movieId) => {
    try {
        const response = await client.get(`/movie/${movieId}`);
        return response.data;
    } catch (error) {
        console.error("Erro ao buscar detalhes do filme:", error);
        return null;
    }
};

// NOVA FUNÇÃO para buscar um filme pelo nome
export const searchMovie = async (query) => {
    try {
        const response = await client.get('/search/movie', {
            params: { query: query }
        });
        // Retorna o primeiro resultado da busca
        return response.data.results[0];
    } catch (error) {
        console.error("Erro ao buscar filme:", error);
        return null;
    }
}

// Endpoints para as diferentes listas de filmes que queremos
export const endpoints = {
    popular: '/movie/popular',
    topRated: '/movie/top_rated',
    trending: '/trending/movie/week',
    action: '/discover/movie?with_genres=28',
    comedy: '/discover/movie?with_genres=35',
};

// URL base para as imagens dos posters
export const getImageUrl = (path, size = 'w500') => `https://image.tmdb.org/t/p/${size}${path}`;
