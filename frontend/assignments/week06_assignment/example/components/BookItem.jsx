import React, { memo } from 'react';
import { Trash2, Star, Heart, BookOpen, BookMarked, CheckCircle } from 'lucide-react';

const BookItem = memo(({ book, onDelete, onToggleFavorite, onStatusChange }) => {
  const handleDelete = () => {
    if (window.confirm(`"${book.title}"을(를) 삭제하시겠습니까?`)) {
      onDelete(book.id);
    }
  };

  const getStatusIcon = () => {
    switch (book.status) {
      case 'toRead':
        return <BookMarked className="status-icon" />;
      case 'reading':
        return <BookOpen className="status-icon reading" />;
      case 'completed':
        return <CheckCircle className="status-icon completed" />;
      default:
        return null;
    }
  };

  const getStatusLabel = () => {
    switch (book.status) {
      case 'toRead':
        return '읽을 예정';
      case 'reading':
        return '읽는 중';
      case 'completed':
        return '완독';
      default:
        return '';
    }
  };

  return (
    <div className={`book-item ${book.isFavorite ? 'favorite' : ''}`}>
      <div className="book-header">
        <div className="book-info">
          <h3 className="book-title">{book.title}</h3>
          <p className="book-author">저자: {book.author}</p>
        </div>
        
        <div className="book-actions">
          <button
            onClick={() => onToggleFavorite(book.id)}
            className={`icon-button favorite-button ${book.isFavorite ? 'active' : ''}`}
            aria-label="즐겨찾기"
          >
            <Heart size={18} />
          </button>
          <button
            onClick={handleDelete}
            className="icon-button delete-button"
            aria-label="삭제"
          >
            <Trash2 size={18} />
          </button>
        </div>
      </div>

      <div className="book-status">
        {getStatusIcon()}
        <select
          value={book.status}
          onChange={(e) => onStatusChange(book.id, e.target.value)}
          className="status-select"
        >
          <option value="toRead">읽을 예정</option>
          <option value="reading">읽는 중</option>
          <option value="completed">완독</option>
        </select>
      </div>

      <div className="book-rating">
        <span className="rating-label">평점:</span>
        <div className="rating-stars">
          {[...Array(5)].map((_, index) => (
            <Star
              key={index}
              className={`star ${index < book.rating ? 'filled' : ''}`}
              size={16}
            />
          ))}
          <span className="rating-value">({book.rating}점)</span>
        </div>
      </div>

      {book.memo && (
        <div className="book-memo">
          <p>{book.memo}</p>
        </div>
      )}

      <div className="book-footer">
        <span className="book-date">등록일: {book.createdAt}</span>
        <span className={`status-badge ${book.status}`}>
          {getStatusLabel()}
        </span>
      </div>
    </div>
  );
});

BookItem.displayName = 'BookItem';

export default BookItem;