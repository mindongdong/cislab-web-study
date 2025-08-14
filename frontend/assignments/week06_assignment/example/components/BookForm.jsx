import React, { useState, useRef, memo, useCallback } from 'react';
import { Plus } from 'lucide-react';
import { useBooks } from '../context/BookContext';

const BookForm = memo(() => {
  const { addBook } = useBooks();
  const titleInputRef = useRef(null);
  
  const [formData, setFormData] = useState({
    title: '',
    author: '',
    rating: 5,
    memo: '',
    status: 'toRead'
  });

  const [isExpanded, setIsExpanded] = useState(false);

  const handleChange = useCallback((e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  }, []);

  const handleSubmit = useCallback((e) => {
    e.preventDefault();
    
    if (!formData.title.trim() || !formData.author.trim()) {
      alert('제목과 저자를 모두 입력해주세요.');
      return;
    }

    const newBook = {
      ...formData,
      id: Date.now(),
      createdAt: new Date().toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      }).replace(/\. /g, '/').replace('.', ''),
      isFavorite: false,
      rating: Number(formData.rating)
    };

    addBook(newBook);

    // Reset form
    setFormData({
      title: '',
      author: '',
      rating: 5,
      memo: '',
      status: 'toRead'
    });

    // Focus back to title input
    titleInputRef.current?.focus();
  }, [formData, addBook]);

  return (
    <div className="book-form-container">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="form-toggle-button"
      >
        <Plus className="form-icon" />
        새 책 추가하기
      </button>

      {isExpanded && (
        <form onSubmit={handleSubmit} className="book-form">
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="title">책 제목 *</label>
              <input
                ref={titleInputRef}
                id="title"
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                className="form-input"
                placeholder="예: 해리포터와 마법사의 돌"
                autoFocus
              />
            </div>

            <div className="form-group">
              <label htmlFor="author">저자 *</label>
              <input
                id="author"
                type="text"
                name="author"
                value={formData.author}
                onChange={handleChange}
                className="form-input"
                placeholder="예: J.K. 롤링"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="rating">별점</label>
              <select
                id="rating"
                name="rating"
                value={formData.rating}
                onChange={handleChange}
                className="form-select"
              >
                {[5, 4, 3, 2, 1].map(num => (
                  <option key={num} value={num}>
                    {'⭐'.repeat(num)} ({num}점)
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="status">읽기 상태</label>
              <select
                id="status"
                name="status"
                value={formData.status}
                onChange={handleChange}
                className="form-select"
              >
                <option value="toRead">읽을 예정</option>
                <option value="reading">읽는 중</option>
                <option value="completed">완독</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="memo">읽고 난 감상</label>
            <textarea
              id="memo"
              name="memo"
              value={formData.memo}
              onChange={handleChange}
              rows="3"
              className="form-textarea"
              placeholder="책을 읽고 느낀 점을 자유롭게 작성해주세요..."
            />
          </div>

          <div className="form-actions">
            <button type="submit" className="submit-button">
              책 추가하기
            </button>
            <button
              type="button"
              onClick={() => setIsExpanded(false)}
              className="cancel-button"
            >
              취소
            </button>
          </div>
        </form>
      )}
    </div>
  );
});

BookForm.displayName = 'BookForm';

export default BookForm;