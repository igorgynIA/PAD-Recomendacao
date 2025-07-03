import React, { useState, useEffect, useRef } from 'react';
import { FaSearch, FaTimes } from 'react-icons/fa';
import './SearchBar.css';

const SearchBar = ({ onSearch, onClose, isOpen }) => {
    const [query, setQuery] = useState('');
    const inputRef = useRef(null);

    useEffect(() => {
        if (isOpen) {
            inputRef.current.focus();
        }
    }, [isOpen]);

    const handleSearch = (e) => {
        e.preventDefault();
        if (query) {
            onSearch(query);
            setQuery('');
        }
    };

    return (
        <form
            className={`search-bar-container ${isOpen ? 'open' : ''}`}
            onSubmit={handleSearch}
        >
            <FaSearch className="search-icon" onClick={handleSearch} />
            <input
                ref={inputRef}
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Títulos, gente e gêneros"
                className="search-input"
            />
            <FaTimes className="close-search-icon" onClick={onClose} />
        </form>
    );
};

export default SearchBar;
