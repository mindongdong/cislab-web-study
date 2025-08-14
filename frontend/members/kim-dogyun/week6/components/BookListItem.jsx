import BookItem from "./BookItem";
import { useRef, useEffect, memo, useContext } from "react";
import { DataSetContext, DataStateContext } from "../App";
import { SearchContext } from "./BookList";

function BookListItem() {
  const { books, search, searchMode } = useContext(DataStateContext);
  const { setAnimationHeight, setAtTop } = useContext(DataSetContext);
  const { searchRating, searchStatus } = useContext(SearchContext);
  const ref = useRef();

  useEffect(() => {
    if (ref.current) {
      const rect = ref.current.getBoundingClientRect();
      setAnimationHeight(
        rect.bottom
        //books.length > 0 ? `${rect.top}px` : `${rect.top}px - 3em`
      );
      console.log("요소의 좌표:", rect.top);
      console.log(window.screen.height);
    }
  }, [books.length, setAnimationHeight]);

  const handleScroll = (e) => {
    const scrollTop = e.target.scrollTop;
    setAtTop(scrollTop === 0);
    console.log(scrollTop);
  };

  const getFilteredData = () => {
    let updatedBooks = books.map((book) => ({ ...book }));

    switch (searchMode) {
      case "none":
        updatedBooks = updatedBooks.map((book) => {
          book.hidden = false;
          return book;
        });
        break;
      case "liked":
        updatedBooks = updatedBooks.map((book) => {
          const match = book.liked == true;
          book.hidden = !match;
          return book;
        });
        break;

      case "name":
        if (search == "") {
          updatedBooks = updatedBooks.map((book) => {
            book.hidden = false;
            return book;
          });
          break;
        } else {
          updatedBooks = updatedBooks.map((book) => {
            const match = book.name.includes(search);
            book.hidden = !match;
            return book;
          });
          break;
        }

      case "author":
        if (search == "") {
          updatedBooks = updatedBooks.map((book) => {
            book.hidden = false;
            return book;
          });
          break;
        } else {
          updatedBooks = updatedBooks.map((book) => {
            const match = book.author.includes(search);
            book.hidden = !match;
            return book;
          });
          break;
        }

      case "rating":
        switch (searchRating) {
          case "all":
            updatedBooks = updatedBooks.map((book) => {
              book.hidden = false;
              return book;
            });
            break;

          case "5":
            updatedBooks = updatedBooks.map((book) => {
              const match = book.rating >= 99;
              book.hidden = !match;
              return book;
            });
            break;

          case "4":
            updatedBooks = updatedBooks.map((book) => {
              const match = 99 > book.rating && book.rating >= 80;
              book.hidden = !match;
              return book;
            });
            break;

          case "3":
            updatedBooks = updatedBooks.map((book) => {
              const match = 80 > book.rating && book.rating >= 60;
              book.hidden = !match;
              return book;
            });
            break;

          case "2":
            updatedBooks = updatedBooks.map((book) => {
              const match = 60 > book.rating && book.rating >= 40;
              book.hidden = !match;
              return book;
            });
            break;

          case "1":
            updatedBooks = updatedBooks.map((book) => {
              const match = 40 > book.rating && book.rating >= 20;
              book.hidden = !match;
              return book;
            });
            break;

          case "0":
            updatedBooks = updatedBooks.map((book) => {
              const match = 20 > book.rating;
              book.hidden = !match;
              return book;
            });
            break;

          default:
            updatedBooks = updatedBooks.map((book) => {
              book.hidden = false;
              return book;
            });
            break;
        }
        break;

      case "status":
        switch (searchStatus) {
          case "all":
            updatedBooks = updatedBooks.map((book) => {
              book.hidden = false;
              return book;
            });
            break;
          case "2":
            updatedBooks = updatedBooks.map((book) => {
              const match = book.status == "2";
              book.hidden = !match;
              return book;
            });
            break;

          case "1":
            updatedBooks = updatedBooks.map((book) => {
              const match = book.status == "1";
              book.hidden = !match;
              return book;
            });
            break;

          case "0":
            updatedBooks = updatedBooks.map((book) => {
              const match = book.status == "0";
              book.hidden = !match;
              return book;
            });
            break;

          default:
            updatedBooks = updatedBooks.map((book) => {
              book.hidden = false;
              return book;
            });
            break;
        }
    }

    return updatedBooks;
  };

  return (
    <>
      <div className="bookListItem" onScroll={handleScroll}>
        <div ref={ref} style={{ height: "7.75em" }}></div>
        {Array.isArray(books) && books.length > 0 ? (
          getFilteredData().map((book) => (
            <BookItem key={book.id} books={book} />
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
          className="bookListItemLocateHelper"
          style={{ height: "3em" }}
        ></div>
      </div>
    </>
  );
}

export default memo(BookListItem);
