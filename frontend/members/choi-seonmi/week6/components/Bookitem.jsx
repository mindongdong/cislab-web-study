import './Bookitem.css'
import { memo, useContext } from 'react';
import { BookContext, ThemeContext } from '../App';

const Bookitem = ({ book, highlight }) => {
  const { onClickDelButton, toggleFavorite }  = useContext(BookContext) 
  const { theme } = useContext(ThemeContext)

  return (
     <div className={`card card-${theme} ${highlight ? `highlight highlight-${theme}` : ''} 
     ${book.isFavorite ? `favorite favorite-${theme}` : ''}`}>
      <div className="Bookitem-text">
        <button
          className={`button-del button-del-${theme}`}
          onClick={() => onClickDelButton(book.id)}
        >
          ╳
        </button>
        <button
            className={`button-favorite button-favorite-${theme} ${book.isFavorite ? 'active' : ''}`}
            onClick={() => toggleFavorite(book.id)}
          >
            {book.isFavorite ? <i class="fa-solid fa-bookmark"></i> : <i class="fa-regular fa-bookmark"></i>}
        </button>
        <p> ◈ 제목: {book.title}</p>
        <p> ◈ 저자: {book.author}</p>
        <p> ◈ 별점: {"★".repeat(book.star)}</p>
        <p> ◈ 메모: {book.memo}</p>
      </div>
    </div>
  );
};

export default memo(Bookitem);