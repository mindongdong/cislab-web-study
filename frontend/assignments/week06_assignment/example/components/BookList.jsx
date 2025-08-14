import React, { memo, useCallback } from 'react';
import { BookOpen } from 'lucide-react';
import BookItem from './BookItem';
import { useBooks } from '../context/BookContext';

const BookList = memo(() => {
  const { filteredBooks, deleteBook, toggleFavorite, updateStatus } = useBooks();

  // Memoized callbacks for child components
  const handleDelete = useCallback((id) => {
    deleteBook(id);
  }, [deleteBook]);

  const handleToggleFavorite = useCallback((id) => {
    toggleFavorite(id);
  }, [toggleFavorite]);

  const handleStatusChange = useCallback((id, status) => {
    updateStatus(id, status);
  }, [updateStatus]);

  if (filteredBooks.length === 0) {
    return (
      <div className="empty-state">
        <BookOpen className="empty-icon" />
        <p className="empty-title">검색 결과가 없습니다</p>
        <p className="empty-subtitle">
          다른 검색어나 필터를 시도해보세요
        </p>
      </div>
    );
  }

  return (
    <div className="book-list">
      {filteredBooks.map(book => (
        <BookItem
          key={book.id}
          book={book}
          onDelete={handleDelete}
          onToggleFavorite={handleToggleFavorite}
          onStatusChange={handleStatusChange}
        />
      ))}
    </div>
  );
});

BookList.displayName = 'BookList';

export default BookList;