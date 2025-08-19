import { useState } from "react";
import { useRef } from "react";

function BookForm({ onAddBook }) {
  const [input, setInput] = useState({
    name: "",
    author: "",
    rating: 0,
    review: "",
  });

  const bookRating = 5.5 * (input.rating / 100);
  const inputRef = useRef();

  const onChange = (e) => {
    setInput({
      ...input,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = () => {
    onAddBook(input);
    setInput({
      name: "",
      author: "",
      rating: 0,
      review: "",
    });
    inputRef.current.focus();
  };

  return (
    <>
      <div className="bookForm">
        <div className="bookFormTitle">
          <div
            style={{
              color: "#3e3f29",
              margin: "0.5em 0 0 0",
              fontFamily: "Pretendard-Bold",
              fontSize: "2em",
            }}
          >
            새로운 책 등록
          </div>
          <div className="bookFormTitleButton" onClick={handleSubmit}>
            <img
              src="./src/assets/save.svg"
              style={{ height: "1em", margin: "0 0.5em 0.05em 0" }}
            />
            등록
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
          <div style={{ color: "#b6a085" }}>별점</div>
          <div className="bookFormInputRating">
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
            <div
              style={{ minWidth: "5em", margin: "0 0 0 1em", color: "#b6a085" }}
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
              style={{ minWidth: "4em", color: "#b6a085", textAlign: "right" }}
            >
              추천해요!
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

export default BookForm;
