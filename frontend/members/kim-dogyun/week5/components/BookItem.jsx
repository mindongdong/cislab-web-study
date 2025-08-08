import { useRef, useEffect, useState } from "react";

function BookItem({ books, deleteMode, onDeleteBooks }) {
  const bookName = books.name;
  const bookAuthor = books.author;
  const bookRating = 5.5 * (books.rating / 100);
  const bookReview = books.review;
  const ref = useRef();

  const [isDeleting, setIsDeleting] = useState(false);
  const [appearClass, setAppearClass] = useState("before-appear");

  useEffect(() => {
    requestAnimationFrame(() => {
      setTimeout(() => {
        setAppearClass("appear");
      }, 285);
    });
  }, []);

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
      onDeleteBooks(books);
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
          marginBottom: deleteMode == true ? "1em" : "0",
        }}
      >
        <div className="bookItem">
          <div className="bookItemLeft">
            <div className="bookItemLeftName">{bookName}</div>
            <div className="bookItemLeftReview">{bookReview}</div>
          </div>
          <div className="bookItemRight">
            <div className="bookItemRightAuthor">{bookAuthor}</div>
            <div className="bookItemRightRating">
              <div className="bookItemRightRatingStar">
                <img src="./src/assets/star.svg" />
                <div
                  className="bookItemRightRatingColorFilled"
                  style={{ width: `${bookRating}em` }}
                ></div>
                <div className="bookItemRightRatingColor"></div>
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
            }}
          >
            <img
              style={{ height: "1.15em", margin: "0 0.25em 0 0" }}
              src="./src/assets/trashWhite.svg"
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

export default BookItem;
