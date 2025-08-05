
const Bookitem = ({books, onClickDelButton}) => {
    if (books.length == 0) {
        return (
            <div className='Booklist'>
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
            <div className='Bookitem'>
                <h3>☰ &nbsp; 읽은 책의 목록</h3>
                <div>
                    <p>✔ 읽은 책: {books.length}권</p>
                    {books.map((book) => (
                        <div key={book.id} className="card">
                            <div className='Bookitem-text'>
                                <button 
                                    className='button-del' 
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