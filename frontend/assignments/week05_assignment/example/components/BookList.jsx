import React from 'react';
import { BookOpen } from 'lucide-react';
import BookItem from './BookItem';

// BookList 컴포넌트 - 책 목록 표시
const BookList = ({ books, onDeleteBook }) => {
  if (books.length === 0) {
    return (
      <div className="bg-gray-50 rounded-lg p-12 text-center">
        <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600 text-lg">아직 등록된 책이 없습니다</p>
        <p className="text-gray-500 text-sm mt-2">
          위의 폼을 통해 첫 번째 책을 추가해보세요!
        </p>
      </div>
    );
  }
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {books.map(book => (
        <BookItem
          key={book.id}
          book={book}
          onDeleteBook={onDeleteBook}
        />
      ))}
    </div>
  );
};

export default BookList;