import React, { useState, useRef } from 'react';
import { Plus } from 'lucide-react';

// BookForm 컴포넌트 - 책 정보 입력 폼
const BookForm = ({ onAddBook }) => {
  const [formData, setFormData] = useState({
    title: '',
    author: '',
    rating: 5,
    memo: ''
  });
  
  // useRef를 사용하여 입력 필드 참조
  const titleInputRef = useRef(null);
  
  // 입력 필드 변경 핸들러
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  // 폼 제출 핸들러
  const handleSubmit = () => {
    // 유효성 검사
    if (!formData.title.trim() || !formData.author.trim()) {
      alert('제목과 저자를 모두 입력해주세요.');
      return;
    }
    
    // 책 추가
    onAddBook({
      ...formData,
      id: Date.now(),
      createdAt: new Date().toLocaleDateString()
    });
    
    // 폼 초기화
    setFormData({
      title: '',
      author: '',
      rating: 5,
      memo: ''
    });
    
    // 첫 번째 입력 필드에 포커스
    titleInputRef.current?.focus();
  };
  
  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
        <Plus className="w-5 h-5" />
        새 책 추가하기
      </h2>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">
            책 제목 *
          </label>
          <input
            ref={titleInputRef}
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="예: 해리포터와 마법사의 돌"
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                handleSubmit();
              }
            }}
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-1">
            저자 *
          </label>
          <input
            type="text"
            name="author"
            value={formData.author}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="예: J.K. 롤링"
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                handleSubmit();
              }
            }}
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-1">
            별점 (1-5점)
          </label>
          <select
            name="rating"
            value={formData.rating}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {[5, 4, 3, 2, 1].map(num => (
              <option key={num} value={num}>
                {'⭐'.repeat(num)} ({num}점)
              </option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-1">
            읽고 난 감상
          </label>
          <textarea
            name="memo"
            value={formData.memo}
            onChange={handleChange}
            rows="3"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="책을 읽고 느낀 점을 자유롭게 작성해주세요..."
          />
        </div>
        
        <button
          onClick={handleSubmit}
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition-colors font-medium"
        >
          책 추가하기
        </button>
      </div>
    </div>
  );
};

export default BookForm;