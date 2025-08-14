import "./../stylesheets/BookItem.css";
import { useRef, useEffect, useState, memo, useContext } from "react";
import { ThemeStateContext, DataStateContext, DataSetContext } from "../App";

function BookItem({ books }) {
  const { darkMode } = useContext(ThemeStateContext);
  const { deleteMode, editBook, onEditMode } = useContext(DataStateContext);
  const { handleDeleteBook, setOnEditMode, setEditBook, setClickedBookItem } =
    useContext(DataSetContext);

  const bookName = books.name;
  const bookAuthor = books.author;
  const bookRating = 5.5 * (books.rating / 100);
  const bookReview = books.review;
  const bookLiked = books.liked;
  const bookStatus = books.status;
  const ref = useRef();

  const [isDeleting, setIsDeleting] = useState(false);
  const [appearClass, setAppearClass] = useState("before-appear");
  const heightRef = useRef(0);
  const isInitialMount = useRef(true);

  useEffect(() => {
    const element = ref.current;
    heightRef.current = element.scrollHeight;
    element.style.height = "0px";
    requestAnimationFrame(() => {
      element.style.height = heightRef.current + "px";
      setTimeout(() => {
        setAppearClass("appear");
        element.style.height = "auto";
      }, 285);
    });
  }, []);

  useEffect(() => {
    if (isInitialMount.current) {
      isInitialMount.current = false;
      return;
    }

    const element = ref.current;
    if (books.hidden) {
      if (deleteMode) {
        element.style.height = `${heightRef.current + 16}px`;
      } else {
        element.style.height = `${heightRef.current}px`;
      }
      element.style.transform = "scale(1)";
      element.style.opacity = "1";
      requestAnimationFrame(() => {
        element.style.height = "0px";
        element.style.transform = "scale(0)";
        element.style.opacity = "0";
        // setTimeout(() => {
        //   element.style.transform = "";
        //   element.style.opacity = "";
        // }, 300);
      });
    } else {
      requestAnimationFrame(() => {
        if (deleteMode) {
          element.style.height = `${heightRef.current + 16}px`;
        } else {
          element.style.height = `${heightRef.current}px`;
        }
        setTimeout(() => {
          element.style.transform = "scale(1)";
          element.style.opacity = "1";
        });

        setTimeout(() => {
          element.style.height = "auto";
          element.style.transform = "";
          element.style.opacity = "";
        }, 300);
      });
    }
    // eslint-disable-next-line
  }, [books.hidden]);

  useEffect(() => {
    if (onEditMode && books.id == editBook.id) {
      ref.current.style.left = "0";
      setTimeout(() => {
        ref.current.style.opacity = "0";
        ref.current.style.left = "200px";
      }, 150);
    } else if (!onEditMode && books.id == editBook.id) {
      ref.current.style.height = "auto";
      const newHeight = ref.current.scrollHeight;
      requestAnimationFrame(() => {
        ref.current.style.height = `${heightRef.current}px`;
        setTimeout(() => {
          ref.current.style.height = `${newHeight}px`;
          heightRef.current = newHeight;
          ref.current.style.opacity = "";
          ref.current.style.left = "0";
          setTimeout(() => {
            ref.current.style.height = "auto";
          }, 400);
        }, 325);
      });
    }
    // eslint-disable-next-line
  }, [onEditMode]);

  const handleEdit = () => {
    const item = ref.current.getBoundingClientRect();
    setClickedBookItem(item);
    requestAnimationFrame(() => {
      setOnEditMode(true);
      setEditBook({
        id: books.id,
        name: books.name,
        author: books.author,
        rating: books.rating,
        review: books.review,
        liked: books.liked,
        status: books.status,
        hidden: books.hidden,
      });
    });
  };

  const handleDelete = () => {
    const element = ref.current;
    const height = element.scrollHeight;
    element.style.height = height + "px";

    requestAnimationFrame(() => {
      setIsDeleting(true);
      element.style.height = "0px";
      element.style.marginBottom = "0px";
    });

    setTimeout(() => {
      handleDeleteBook(books);
    }, 300);
  };

  return (
    <>
      <div
        ref={ref}
        className={`bookItemWrapper ${appearClass} ${
          isDeleting ? "fade-out" : ""
        }`}
        style={{
          position: "relative",
          marginBottom: deleteMode && !books.hidden == true ? "1em" : "0",
        }}
      >
        <div
          className="bookItem"
          onClick={handleEdit}
          style={{ pointerEvents: deleteMode || onEditMode ? "none" : "auto" }}
        >
          <div className="bookItemLeft">
            <div className="bookItemLeftName">{bookName}</div>
            <div className="bookItemLeftReview">{bookReview}</div>
          </div>
          <div className="bookItemDownWrapper">
            <div className="bookItemDown">
              {bookLiked ? (
                <img
                  src={
                    darkMode
                      ? "./src/assets/darkmode/heart.svg"
                      : "./src/assets/heart.svg"
                  }
                />
              ) : (
                ""
              )}
              {bookStatus == "0"
                ? "읽을 예정"
                : bookStatus == "1"
                ? "읽는 중"
                : "완독"}
            </div>
            <div className="bookItemRight">
              <div className="bookItemRightAuthor">{bookAuthor}</div>
              <div className="bookItemRightRating">
                <div className="bookItemRightRatingStar">
                  <img
                    src={
                      darkMode
                        ? "./src/assets/darkmode/star.svg"
                        : "./src/assets/star.svg"
                    }
                  />
                  <div
                    className="bookItemRightRatingColorFilled"
                    style={{ width: `${bookRating}em` }}
                  ></div>
                  <div className="bookItemRightRatingColor"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <>
          <div
            className="bookItemDelete"
            onClick={handleDelete}
            style={{
              pointerEvents: deleteMode ? "all" : "none",
              padding: deleteMode ? "2em 1em 0.5em 1em" : "0",
              bottom: deleteMode ? "0" : "3em",
              opacity: deleteMode ? "1" : "0",
            }}
          >
            <img
              style={{ height: "1.15em", margin: "0 0.25em 0 0" }}
              src={
                darkMode
                  ? "./src/assets/darkmode/trashWhite.svg"
                  : "./src/assets/trashWhite.svg"
              }
            />
            삭제
          </div>
          <div
            className={`bookItemDeleteHelper ${isDeleting ? "fade-out" : ""}`}
            style={{ height: deleteMode ? "1em" : "0" }}
          ></div>
        </>
      </div>
    </>
  );
}

export default memo(BookItem);
