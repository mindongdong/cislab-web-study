import React, { memo } from 'react';
import { Search, Filter, Heart } from 'lucide-react';
import { useBooks } from '../context/BookContext';

const SearchFilter = memo(() => {
  const {
    searchTerm,
    filterStatus,
    filterRating,
    showFavoritesOnly,
    setSearchTerm,
    setFilterStatus,
    setFilterRating,
    setShowFavoritesOnly
  } = useBooks();

  return (
    <div className="search-filter">
      <div className="search-container">
        <Search className="search-icon" />
        <input
          type="text"
          placeholder="제목 또는 저자로 검색..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      <div className="filter-container">
        <Filter className="filter-icon" />
        
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          className="filter-select"
        >
          <option value="all">모든 상태</option>
          <option value="toRead">읽을 예정</option>
          <option value="reading">읽는 중</option>
          <option value="completed">완독</option>
        </select>

        <select
          value={filterRating}
          onChange={(e) => setFilterRating(Number(e.target.value))}
          className="filter-select"
        >
          <option value="0">모든 별점</option>
          <option value="5">⭐⭐⭐⭐⭐ 5점</option>
          <option value="4">⭐⭐⭐⭐ 4점 이상</option>
          <option value="3">⭐⭐⭐ 3점 이상</option>
          <option value="2">⭐⭐ 2점 이상</option>
          <option value="1">⭐ 1점 이상</option>
        </select>

        <button
          onClick={() => setShowFavoritesOnly(!showFavoritesOnly)}
          className={`filter-button ${showFavoritesOnly ? 'active' : ''}`}
          aria-label="즐겨찾기만 보기"
        >
          <Heart size={18} />
          즐겨찾기
        </button>
      </div>
    </div>
  );
});

SearchFilter.displayName = 'SearchFilter';

export default SearchFilter;