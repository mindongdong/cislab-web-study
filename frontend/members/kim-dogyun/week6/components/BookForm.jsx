import "./../stylesheets/BookForm.css";
import { useState, useRef, useEffect, useContext, memo } from "react";
import { ThemeStateContext, DataStateContext, DataSetContext } from "../App";

function BookForm() {
  const { darkMode } = useContext(ThemeStateContext);
  const { onEditMode, editBook } = useContext(DataStateContext);
  const { handleAddBook, handleEditBook } = useContext(DataSetContext);
  const [input, setInput] = useState({
    name: "",
    author: "",
    rating: 0,
    review: "",
    liked: false,
    status: "0",
    hidden: false,
  });

  const bookRating = 5.5 * (input.rating / 100);
  const inputRef = useRef();

  useEffect(() => {
    if (onEditMode) {
      setTimeout(() => {
        setInput(editBook);
      }, 570);
    }
    // eslint-disable-next-line
  }, [onEditMode]);

  const onChange = (e) => {
    setInput({
      ...input,
      [e.target.name]: e.target.value,
    });
    console.log(`${e.target.name} : ${e.target.value}`);
  };

  const onChangeLiked = () => {
    setInput({
      ...input,
      liked: !input.liked,
    });
  };

  const handleSubmit = () => {
    if (onEditMode) {
      handleEditBook(input);
      setTimeout(() => {
        setInput({
          name: "",
          author: "",
          rating: 0,
          review: "",
          liked: false,
          status: "0",
          hidden: false,
        });
      }, 200);
    } else {
      handleAddBook(input);
      setInput({
        name: "",
        author: "",
        rating: 0,
        review: "",
        liked: false,
        status: "0",
        hidden: false,
      });
    }
    inputRef.current.focus();
  };

  return (
    <>
      <div className="bookForm">
        <div className="bookFormTitle">
          <div
            style={{
              color: "var(--primary-text-color)",
              margin: "0.5em 0 0 0",
              fontFamily: "Pretendard-Bold",
              fontSize: "2em",
            }}
          >
            {onEditMode ? "등록된 책 수정" : "새로운 책 등록"}
          </div>
          <div className="bookFormTitleButton" onClick={handleSubmit}>
            <img
              src={
                darkMode
                  ? "./src/assets/darkmode/save.svg"
                  : "./src/assets/save.svg"
              }
              style={{ height: "1em", margin: "0 0.5em 0.05em 0" }}
            />
            {onEditMode ? "수정" : "등록"}
          </div>
        </div>

        <div className="bookFormInput">
          <div style={{ color: "#b6a085" }}>제목</div>
          <input
            ref={inputRef}
            name="name"
            value={input.name}
            onChange={onChange}
            placeholder="어떤 책을 읽으셨나요?"
          ></input>
        </div>

        <div className="bookFormInput">
          <div style={{ color: "#b6a085" }}>저자</div>
          <input
            name="author"
            value={input.author}
            onChange={onChange}
            placeholder="누가 쓴 책을 읽으셨나요?"
          ></input>
        </div>

        <div className="bookFormInput">
          <div style={{ color: "#b6a085" }}>평가</div>
          <div className="bookFormInputRatingWrapper">
            <div className="bookFormInputRating">
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
              <div
                style={{
                  minWidth: "5em",
                  margin: "0 0 0 1em",
                  color: "#b6a085",
                }}
              >
                별로에요...
              </div>
              <input
                type="range"
                name="rating"
                value={input.rating}
                onChange={onChange}
              ></input>
              <div
                style={{
                  minWidth: "4em",
                  color: "#b6a085",
                  textAlign: "right",
                }}
              >
                추천해요!
              </div>
            </div>
            <div className="bookFormInputStatus">
              <select name="status" onChange={onChange} value={input.status}>
                <option value="0">읽을 예정</option>
                <option value="1">읽는 중</option>
                <option value="2">완독</option>
              </select>
            </div>
            <div className="bookFormInputLiked">
              <div
                className="bookFormInputLikedSelector"
                name="liked"
                value={input.liked}
                onClick={onChangeLiked}
                style={{
                  color: input.liked
                    ? "var(--primary-text-color)"
                    : "var(--highlight-color)",
                }}
              >
                {input.liked ? (
                  <img
                    src={
                      darkMode
                        ? "./src/assets/darkmode/heart.svg"
                        : "./src/assets/heart.svg"
                    }
                  />
                ) : (
                  <img
                    src={
                      darkMode
                        ? "./src/assets/darkmode/unheart.svg"
                        : "./src/assets/unheart.svg"
                    }
                  />
                )}
                즐겨찾기
              </div>
            </div>
          </div>
        </div>

        <div
          className="bookFormInput"
          style={{ flexGrow: "1", alignItems: "flex-start" }}
        >
          <div style={{ color: "#b6a085", margin: "1em 0 0 0" }}>감상평</div>
          <textarea
            name="review"
            value={input.review}
            onChange={onChange}
            placeholder="이 책은 어떻게 감상하셨나요?"
          ></textarea>
        </div>
      </div>
    </>
  );
}

export default memo(BookForm);
