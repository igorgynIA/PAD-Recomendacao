import React, { useState, useEffect } from 'react';
import './Homepage.css';
import { FaSearch, FaBell, FaUser, FaChevronLeft, FaChevronRight } from 'react-icons/fa';
import { fetchMovies, endpoints, getImageUrl, getMovieDetails, searchMovie } from '../tmdb';
import logo from '../imgs/logo.png';
import Card from './Card';
import './Card.css';
import SearchBar from './SearchBar';
import './SearchBar.css';

// Componente MovieRow atualizado com a lógica do carrossel
const MovieRow = ({ title, movies, onPosterClick }) => {
    const [scrollX, setScrollX] = useState(0);

    const handleLeftArrow = () => {
        let x = scrollX + Math.round(window.innerWidth / 2);
        if (x > 0) {
            x = 0;
        }
        setScrollX(x);
    };

    const handleRightArrow = () => {
        let x = scrollX - Math.round(window.innerWidth / 2);
        const listWidth = movies.length * 180; // Largura de cada poster
        if ((window.innerWidth - listWidth) > x) {
            x = (window.innerWidth - listWidth) - 60; // 60px de padding
        }
        setScrollX(x);
    };

    return (
        <div className="movie-row">
            <h2>{title}</h2>
            <div className="movie-row--left" onClick={handleLeftArrow}>
                <FaChevronLeft style={{ fontSize: 30 }} />
            </div>
            <div className="movie-row--right" onClick={handleRightArrow}>
                <FaChevronRight style={{ fontSize: 30 }} />
            </div>
            <div className="movie-row--listarea">
                <div className="movie-row--list" style={{
                    marginLeft: scrollX,
                    width: movies.length * 180
                }}>
                    {movies.map((movie) => (
                        <div key={movie.id} className="poster-container" onClick={() => onPosterClick(movie)}>
                            <img src={getImageUrl(movie.poster_path)} alt={movie.title || movie.name} />
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

function Homepage() {
    // ... (todo o resto do seu código permanece igual)
    const [topTierMovies, setTopTierMovies] = useState([]);
    const [midTierMovies, setMidTierMovies] = useState([]);
    const [lowTierMovies, setLowTierMovies] = useState([]);
    const [mainMovie, setMainMovie] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [selectedMovie, setSelectedMovie] = useState(null);
    const [isSearchOpen, setIsSearchOpen] = useState(false);

    const handleOpenModal = (movie) => setSelectedMovie(movie);
    const handleCloseModal = () => setSelectedMovie(null);

    const handleSearch = async (query) => {
        const movieResult = await searchMovie(query);
        if (movieResult) {
            handleOpenModal(movieResult);
        } else {
            alert('Filme não encontrado!');
        }
        setIsSearchOpen(false);
    };

    useEffect(() => {
        if (selectedMovie) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'auto';
        }
        return () => {
            document.body.style.overflow = 'auto';
        };
    }, [selectedMovie]);

    useEffect(() => {
        const loadData = async () => {
            setIsLoading(true);
            const response = await fetch('/movie_ids.json');
            const allIds = await response.json();

            const topTierIds = new Set(allIds.slice(0, 500));
            const midTierIds = new Set(allIds.slice(500, 1000));
            const lowTierIds = new Set(allIds.slice(1000, 1500));

            const pagesToFetch = [1, 2, 3, 4, 5, 6, 7];
            const endpointsToFetch = [
                endpoints.popular,
                endpoints.topRated,
                endpoints.trending,
                endpoints.action,
                endpoints.comedy,
            ];

            const fetchPromises = endpointsToFetch.flatMap(endpoint =>
                pagesToFetch.map(page => {
                    const separator = endpoint.includes('?') ? '&' : '?';
                    return fetchMovies(`${endpoint}${separator}page=${page}`);
                })
            );

            const movieLists = await Promise.all(fetchPromises);

            const allFetchedMoviesMap = new Map();
            movieLists.flat().forEach(movie => {
                if (movie) {
                    allFetchedMoviesMap.set(movie.id, movie);
                }
            });
            const allFetchedMovies = Array.from(allFetchedMoviesMap.values());

            setTopTierMovies(allFetchedMovies.filter(movie => topTierIds.has(String(movie.id))));
            setMidTierMovies(allFetchedMovies.filter(movie => midTierIds.has(String(movie.id))));
            setLowTierMovies(allFetchedMovies.filter(movie => lowTierIds.has(String(movie.id))));

            const interstellarData = await getMovieDetails(157336);
            setMainMovie(interstellarData);
            setIsLoading(false);
        };

        loadData();
    }, []);

    return (
        <div className={`homepage-container ${selectedMovie ? 'modal-open' : ''}`}>
            <header className="header">
                <div className="header-left">
                    <img src={logo} alt="Biaflix Logo" className="logo" />
                    <nav>
                        <a className='me-3' href="#">Início</a>
                        <a className='me-3' href="#">Séries</a>
                        <a href="#" className="active">Filmes</a>
                    </nav>
                </div>
                <div className="header-right">
                    <div className="search-container me-3">
                        <SearchBar 
                            onSearch={handleSearch} 
                            onClose={() => setIsSearchOpen(false)}
                            isOpen={isSearchOpen} 
                        />
                        <FaSearch className="icon" onClick={() => setIsSearchOpen(true)} />
                    </div>
                    <FaBell className="icon me-3" />
                    <FaUser className="icon" />
                </div>
            </header>

            {mainMovie && (
                <main
                    className="hero-banner"
                    style={{ backgroundImage: `url(${getImageUrl(mainMovie.backdrop_path, 'original')})` }}
                >
                    <div className="hero-content">
                        <h1>{mainMovie.name || mainMovie.title}</h1>
                        <p>{mainMovie.overview}</p>
                        <button className="btn btn-light btn-lg" onClick={() => handleOpenModal(mainMovie)}>
                            ▶️ Assistir
                        </button>
                    </div>
                    <div className="hero-fade"></div>
                </main>
            )}

            {!isLoading && (
                <section className="movie-section">
                    <MovieRow title="Principais Filmes" movies={topTierMovies} onPosterClick={handleOpenModal} />
                    <MovieRow title="Continue Explorando" movies={midTierMovies} onPosterClick={handleOpenModal} />
                    <MovieRow title="Sugestões para Você" movies={lowTierMovies} onPosterClick={handleOpenModal} />
                </section>
            )}

            {selectedMovie && <Card movie={selectedMovie} onClose={handleCloseModal} />}
        </div>
    );
}

export default Homepage;
