import React from 'react';
import { BookOpen, Moon, Sun, TrendingUp, Star, Heart } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useBooks } from '../context/BookContext';

const Header = () => {
  const { theme, toggleTheme } = useTheme();
  const { statistics } = useBooks();

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-title">
          <BookOpen className="header-icon" />
          <h1>나의 독서 기록장</h1>
        </div>
        
        <button
          onClick={toggleTheme}
          className="theme-toggle"
          aria-label="테마 변경"
        >
          {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
        </button>
      </div>

      <p className="header-subtitle">
        읽은 책들을 기록하고 감상을 남겨보세요
      </p>

      {/* Statistics Section */}
      <div className="statistics">
        <div className="stat-item">
          <div className="stat-value">{statistics.totalBooks}</div>
          <div className="stat-label">총 책</div>
        </div>
        
        <div className="stat-item">
          <div className="stat-value">{statistics.completedBooks}</div>
          <div className="stat-label">완독</div>
        </div>
        
        <div className="stat-item">
          <div className="stat-value">
            <Star className="stat-icon star" />
            {statistics.averageRating}
          </div>
          <div className="stat-label">평균 별점</div>
        </div>
        
        <div className="stat-item">
          <div className="stat-value">
            <Heart className="stat-icon heart" />
            {statistics.favoriteBooks}
          </div>
          <div className="stat-label">즐겨찾기</div>
        </div>
      </div>

      {statistics.topRatedBook && (
        <div className="top-book">
          <TrendingUp className="top-book-icon" />
          <span>최고 평점 도서: </span>
          <strong>{statistics.topRatedBook.title}</strong>
          <span className="top-book-rating">
            {'⭐'.repeat(statistics.topRatedBook.rating)}
          </span>
        </div>
      )}
    </header>
  );
};

export default Header;