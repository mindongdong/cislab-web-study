
const Bookitem = ({books, onClickDelButton, theme}) => {
    if (books.length == 0) {
        return (
            <div className={`Booklist Booklist-${theme}`}>
                <h3>☰ &nbsp; 읽은 책의 목록</h3>
                <div>
                    <p>✔ 읽은 책: {books.length}권</p>
                    <p className="p-noread">읽은 책이 없어요! ᯅ̈</p>
                </div>
            </div>    
        )
    }
    else {
        return (
            <div className={`Booklist Booklist-${theme}`}>
                <h3>☰ &nbsp; 읽은 책의 목록</h3>
                <div>
                    <p>✔ 읽은 책: {books.length}권</p>
                    {books.map((book) => (
                        <div key={book.id} className={`card card-${theme}`}>
                            <div className='Bookitem-text'>
                                <button 
                                    className={`button-del button-del-${theme}`}
                                    onClick={() => onClickDelButton(book.id)}
                                >
                                    ╳
                                </button>
                                <p> ◈ 제목: {book.title}</p>
                                <p> ◈ 저자: {book.author}</p>
                                <p> ◈ 별점: {'★'.repeat(book.star)}</p>
                                <p> ◈ 메모: {book.memo}</p>

                            </div>                            
                        </div>
                    ))}
                </div>
            </div>
        )
    }
}

export default Bookitem