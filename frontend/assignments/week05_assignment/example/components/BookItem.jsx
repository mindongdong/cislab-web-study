import React from 'react';
import { Trash2, Star } from 'lucide-react';

// BookItem 컴포넌트 - 개별 책 정보 표시
const BookItem = ({ book, onDeleteBook }) => {
  const handleDelete = () => {
    if (window.confirm(`"${book.title}"을(를) 삭제하시겠습니까?`)) {
      onDeleteBook(book.id);
    }
  };
  
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-bold text-gray-800">{book.title}</h3>
          <p className="text-sm text-gray-600">저자: {book.author}</p>
        </div>
        <button
          onClick={handleDelete}
          className="text-red-500 hover:text-red-700 transition-colors p-1"
          aria-label="삭제"
        >
          <Trash2 className="w-5 h-5" />
        </button>
      </div>
      
      <div className="flex items-center gap-2 mb-3">
        <span className="text-sm text-gray-600">평점:</span>
        <div className="flex items-center">
          {[...Array(5)].map((_, index) => (
            <Star
              key={index}
              className={`w-4 h-4 ${
                index < book.rating
                  ? 'text-yellow-400 fill-yellow-400'
                  : 'text-gray-300'
              }`}
            />
          ))}
          <span className="ml-2 text-sm text-gray-600">({book.rating}점)</span>
        </div>
      </div>
      
      {book.memo && (
        <div className="bg-gray-50 rounded p-3">
          <p className="text-sm text-gray-700 whitespace-pre-wrap">{book.memo}</p>
        </div>
      )}
      
      <div className="mt-3 text-xs text-gray-500">
        등록일: {book.createdAt}
      </div>
    </div>
  );
};

export default BookItem;