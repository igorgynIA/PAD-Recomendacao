import React, { useState, useEffect } from 'react';
import './Card.css';
import { FaTimes, FaPlay, FaPlus } from 'react-icons/fa';
import { getImageUrl } from '../tmdb';

const Card = ({ movie, onClose }) => {
    const [recommendations, setRecommendations] = useState([]);
    const [isLoadingRecs, setIsLoadingRecs] = useState(true);

    useEffect(() => {
        // Função para buscar as recomendações do nosso backend
        const fetchRecommendations = async () => {
            if (!movie) return;

            setIsLoadingRecs(true);
            try {
                // Faz a requisição para o servidor Flask usando o ID do filme
                const response = await fetch(`http://localhost:5000/recommend/${movie.id}`);
                const data = await response.json();
                setRecommendations(data);
            } catch (error) {
                console.error("Erro ao buscar recomendações:", error);
                setRecommendations([]); // Limpa em caso de erro
            } finally {
                setIsLoadingRecs(false);
            }
        };

        fetchRecommendations();
    }, [movie]); // Roda sempre que o filme selecionado mudar

    if (!movie) {
        return null;
    }

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <button className="close-button" onClick={onClose}>
                    <FaTimes />
                </button>

                <div
                    className="modal-banner"
                    style={{ backgroundImage: `url(${getImageUrl(movie.backdrop_path, 'original')})` }}
                >
                    <div className="banner-content">
                        <h1>{movie.title || movie.name}</h1>
                        <div className="banner-buttons">
                            <button className="btn btn-light btn-lg me-3">
                                <FaPlay className="me-2" /> Assistir
                            </button>
                            <button className="btn-icon">
                                <FaPlus />
                            </button>
                        </div>
                    </div>
                    <div className="banner-fade"></div>
                </div>

                <div className="modal-details">
                    <p>{movie.overview}</p>

                    {/* Seção de Recomendações */}
                    <div className="recommendations-section">
                        <h3 className="mt-4">Porque você assistiu {movie.title || movie.name}</h3>
                        {isLoadingRecs ? (
                            <p>Buscando recomendações...</p>
                        ) : (
                            <ul>
                                {recommendations.map((rec, index) => (
                                    <li key={index}>{rec}</li>
                                ))}
                            </ul>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Card;
