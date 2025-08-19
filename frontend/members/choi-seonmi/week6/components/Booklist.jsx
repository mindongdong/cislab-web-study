import './Booklist.css'
import Bookitem from "./Bookitem";
import { useState, useEffect, useMemo, memo, useContext } from 'react';
import { BookContext, ThemeContext } from '../App';

const Booklist = () => {
  const { books } = useContext(BookContext)
  const { theme } = useContext(ThemeContext)

  const [totalBooks, setTotalBooks] = useState(0)
  const [meanStar, setMeanStar] = useState(0)

  useEffect(()=> {
    setTotalBooks(books.length)
    
    if (books.length > 0) {
        const totalStars = books.reduce((sum, book) => sum + Number(book.star), 0);
        setMeanStar((totalStars / books.length))
    } else {
        setMeanStar(0)
    }
  }, [books])

  const highStar = Math.max(...books.map(book => book.star))

  const [showOnlyFavorites, setShowOnlyFavorites] = useState(false)
  const filteredBooks = useMemo(() => {
    return showOnlyFavorites 
    ? books.filter(book => book.isFavorite)
    : books
  }, [books, showOnlyFavorites])
  


  const handleFilterToggle = () => {
    setShowOnlyFavorites(!showOnlyFavorites)
  }

  if (books.length === 0) {
    return (
      <div className={`Booklist Booklist-${theme}`}>
        <h3>☰ &nbsp; 읽은 책의 목록</h3>
        <div>
          <p>✔ 읽은 책: {totalBooks}권</p>
          <p>⋆⁺ 평균 별점: {meanStar}권</p>
        <button 
          className={`filter-button filter-button-${theme} ${showOnlyFavorites ? 'active' : ''}`}
          onClick={handleFilterToggle}
        >
          {showOnlyFavorites ? '책갈피 보기' : '책갈피 보기 해제'}
        </button>
          <p className="p-noread">읽은 책이 없어요! ᯅ̈</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`Booklist Booklist-${theme}`}>
      <h3>☰ &nbsp; 읽은 책의 목록</h3>
      <div>
        <p>✔ 읽은 책: {totalBooks}권</p>
        <p>⋆⁺ 평균 별점: {"★".repeat(meanStar)}</p>
        <button 
          className={`filter-button filter-button-${theme} ${showOnlyFavorites ? 'active' : ''}`}
          onClick={handleFilterToggle}
        >
          {showOnlyFavorites ? '전체 보기' : '책갈피 보기'}
        </button>
        {filteredBooks.map((book) => (
          <Bookitem
            book={book}
            highlight={Number(book.star) === highStar}
          />
        ))}
      </div>
    </div>
  );
};

export default memo(Booklist);