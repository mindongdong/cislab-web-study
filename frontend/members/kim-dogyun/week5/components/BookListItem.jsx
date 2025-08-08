import BookItem from "./BookItem";
import { useRef, useEffect } from "react";

function BookListItem({
  books,
  deleteMode,
  onDeleteBooks,
  setAnimationHeight,
}) {
  const ref = useRef();

  useEffect(() => {
    if (ref.current) {
      const rect = ref.current.getBoundingClientRect();
      setAnimationHeight(
        rect.top
        //books.length > 0 ? `${rect.top}px` : `${rect.top}px - 3em`
      );
      console.log("요소의 좌표:", rect.top);
      console.log(window.screen.height);
    }
  }, [books.length]);

  return (
    <>
      <div className="bookListItem">
        <div style={{ height: "7.75em" }}></div>

        {Array.isArray(books) && books.length > 0 ? (
          books.map((books) => (
            <BookItem
              key={books.id}
              books={books}
              deleteMode={deleteMode}
              onDeleteBooks={onDeleteBooks}
            />
          ))
        ) : (
          <div
            style={{
              margin: "2em 0 0 0",
              textAlign: "center",
              color: "#b6a085",
            }}
          >
            등록된 책이 없습니다.
          </div>
        )}
        <div
          ref={ref}
          className="bookListItemLocateHelper"
          style={{ height: "3em" }}
        ></div>
      </div>
    </>
  );
}

export default BookListItem;
