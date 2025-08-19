import React, { useState, useEffect } from 'react';
import { BookOpen } from 'lucide-react';
import BookForm from './components/BookForm';
import BookList from './components/BookList';

// LocalStorage 키 상수
const STORAGE_KEY = 'readingLogBooks';

// App 컴포넌트 - 메인 컴포넌트
const App = () => {
  // LocalStorage에서 초기 데이터 불러오기
  const getInitialBooks = () => {
    try {
      const savedBooks = localStorage.getItem(STORAGE_KEY);
      if (savedBooks) {
        return JSON.parse(savedBooks);
      }
    } catch (error) {
      console.error('LocalStorage 읽기 오류:', error);
    }
    
    // LocalStorage에 데이터가 없거나 오류 발생 시 샘플 데이터 반환
    return [
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
    ];
  };

  const [books, setBooks] = useState(getInitialBooks);
  
  // books 상태가 변경될 때마다 LocalStorage에 저장
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(books));
      console.log('데이터가 LocalStorage에 저장되었습니다.');
    } catch (error) {
      console.error('LocalStorage 저장 오류:', error);
      alert('데이터 저장 중 오류가 발생했습니다. 브라우저의 저장 공간을 확인해주세요.');
    }
  }, [books]);
  
  // 책 추가 함수
  const handleAddBook = (newBook) => {
    setBooks(prev => [newBook, ...prev]);
  };
  
  // 책 삭제 함수
  const handleDeleteBook = (bookId) => {
    setBooks(prev => prev.filter(book => book.id !== bookId));
  };
  
  // LocalStorage 초기화 함수 (디버깅용)
  const handleClearStorage = () => {
    if (window.confirm('모든 데이터를 초기화하시겠습니까? 이 작업은 되돌릴 수 없습니다.')) {
      localStorage.removeItem(STORAGE_KEY);
      setBooks([]);
      alert('모든 데이터가 초기화되었습니다.');
    }
  };
  
  // 통계 계산
  const totalBooks = books.length;
  const averageRating = totalBooks > 0
    ? (books.reduce((sum, book) => sum + Number(book.rating), 0) / totalBooks).toFixed(1)
    : 0;
  
  // LocalStorage 데이터 내보내기 (백업용)
  const handleExportData = () => {
    const dataStr = JSON.stringify(books, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `reading-log-${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };
  
  // LocalStorage 데이터 가져오기 (복원용)
  const handleImportData = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const importedBooks = JSON.parse(e.target.result);
          if (Array.isArray(importedBooks)) {
            setBooks(importedBooks);
            alert('데이터를 성공적으로 가져왔습니다.');
          } else {
            alert('올바른 형식의 파일이 아닙니다.');
          }
        } catch (error) {
          alert('파일을 읽는 중 오류가 발생했습니다.');
        }
      };
      reader.readAsText(file);
    }
  };
  
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
          <p className="text-xs text-gray-500 mt-2">
            💾 데이터는 브라우저에 자동 저장됩니다
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
          
          {/* 데이터 관리 버튼들 */}
          <div className="flex flex-wrap justify-center gap-2 mt-4 pt-4 border-t">
            <button
              onClick={handleExportData}
              className="text-sm px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
              title="데이터를 JSON 파일로 내보내기"
            >
              📥 백업
            </button>
            <label className="text-sm px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors cursor-pointer">
              📤 복원
              <input
                type="file"
                accept=".json"
                onChange={handleImportData}
                className="hidden"
              />
            </label>
            <button
              onClick={handleClearStorage}
              className="text-sm px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
              title="모든 데이터 삭제"
            >
              🗑️ 초기화
            </button>
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