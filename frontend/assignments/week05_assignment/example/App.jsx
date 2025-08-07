import React, { useState } from 'react';
import { BookOpen } from 'lucide-react';
import BookForm from './components/BookForm';
import BookList from './components/BookList';

// App 컴포넌트 - 메인 컴포넌트
const App = () => {
  const [books, setBooks] = useState([
    {
      id: 1,
      title: '클린 코드',
      author: '로버트 마틴',
      rating: 5,
      memo: '개발자라면 꼭 읽어야 할 필독서! 코드 품질에 대한 인식이 완전히 바뀌었습니다.',
      createdAt: '2024/08/01'
    },
    {
      id: 2,
      title: '리팩터링',
      author: '마틴 파울러',
      rating: 4,
      memo: '코드를 개선하는 체계적인 방법을 배울 수 있었습니다.',
      createdAt: '2024/08/03'
    }
  ]);
  
  // 책 추가 함수
  const handleAddBook = (newBook) => {
    setBooks(prev => [newBook, ...prev]);
  };
  
  // 책 삭제 함수
  const handleDeleteBook = (bookId) => {
    setBooks(prev => prev.filter(book => book.id !== bookId));
  };
  
  // 통계 계산
  const totalBooks = books.length;
  const averageRating = totalBooks > 0
    ? (books.reduce((sum, book) => sum + book.rating, 0) / totalBooks).toFixed(1)
    : 0;
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* 헤더 */}
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2 flex items-center justify-center gap-3">
            <BookOpen className="w-10 h-10 text-blue-600" />
            나의 독서 기록장
          </h1>
          <p className="text-gray-600">
            읽은 책들을 기록하고 감상을 남겨보세요
          </p>
        </header>
        
        {/* 통계 섹션 */}
        <div className="bg-white rounded-lg shadow-md p-4 mb-6">
          <div className="flex flex-wrap justify-center gap-8">
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{totalBooks}</p>
              <p className="text-sm text-gray-600">총 읽은 책</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-yellow-500">
                {averageRating}
              </p>
              <p className="text-sm text-gray-600">평균 별점</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">
                {books.filter(book => book.rating === 5).length}
              </p>
              <p className="text-sm text-gray-600">5점 만점 책</p>
            </div>
          </div>
        </div>
        
        {/* 책 추가 폼 */}
        <BookForm onAddBook={handleAddBook} />
        
        {/* 책 목록 */}
        <BookList books={books} onDeleteBook={handleDeleteBook} />
      </div>
    </div>
  );
};

export default App;