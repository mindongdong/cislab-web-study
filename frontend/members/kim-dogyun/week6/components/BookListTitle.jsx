import SearchFilter from "./SearchFilter";
import { useMemo, memo, useContext } from "react";
import {
  DataSetContext,
  DataStateContext,
  ThemeSetContext,
  ThemeStateContext,
} from "../App";

function BookListTitle() {
  const { darkMode } = useContext(ThemeStateContext);
  const { setDarkMode } = useContext(ThemeSetContext);
  const { books, deleteMode, atTop, onStatMode, onEditMode } =
    useContext(DataStateContext);
  const { setDeleteMode, setOnStatMode } = useContext(DataSetContext);

  // const [count, setCount] = useState(0);
  // const [completeCount, setCompleteCount] = useState(0);
  // const [averageRating, setAverageRating] = useState(0);
  // const [maxRating, setMaxRating] = useState("");
  // const [maxRatingName, setMaxRatingName] = useState("");

  const { count, completeCount, averageRating, maxRating, maxRatingName } =
    useMemo(() => {
      if (books.length === 0) {
        const count = 0;
        const completeCount = 0;
        const averageRating = 0;
        const maxRating = 0;
        const maxRatingName = "아직 등록된 책이 없습니다.";
        return {
          count,
          completeCount,
          averageRating,
          maxRating,
          maxRatingName,
        };
      } else {
        const count = books.length;
        const completeCount = books.reduce((count, book) => {
          if (book.status == "2") {
            return count + 1;
          } else {
            return count;
          }
        }, 0);
        const averageRating =
          books
            .map((book) => Number(book.rating))
            .reduce((accumulator, current) => accumulator + current, 0) /
          books.length;

        const maxRatingBook = books.findLast(
          (book) =>
            Number(book.rating) ===
            Math.max(...books.map((book) => Number(book.rating)))
        );
        const maxRating = maxRatingBook.rating;
        const maxRatingName =
          maxRatingBook.name.length > 10
            ? maxRatingBook.name.substring(0, 10) + "···"
            : maxRatingBook.name;
        return {
          count,
          completeCount,
          averageRating,
          maxRating,
          maxRatingName,
        };
      }
    }, [books]);

  const handleDarkMode = () => {
    setDarkMode(darkMode === true ? false : true);
  };

  const handleStatMode = () => {
    setOnStatMode(onStatMode === true ? false : true);
  };

  const handleDeleteMode = () => {
    setDeleteMode(deleteMode === true ? false : true);
  };

  return (
    <>
      <div className="bookListTitle">
        <div className="bookListTitleLogo">
          <div className="lobster-regular">BookBook</div>
          <img src="./src/assets/bookbook.svg" />
        </div>
        <SearchFilter />
        <div
          className="bookListTitleBackground"
          style={{ opacity: atTop ? 0 : 1 }}
        ></div>
        <div
          className="bookListTitleBackgroundBlur"
          style={{ opacity: atTop ? 0 : 1 }}
        ></div>
      </div>
      <div
        className="bookListTitleBottom"
        style={{
          height: onStatMode ? "17em" : "",
          mask: onStatMode ? "linear-gradient(transparent, black 15%)" : "",
          background: onStatMode
            ? "linear-gradient(transparent, var(--foreground-color) 30%"
            : "",
        }}
      >
        <div
          className="bookListTitleBottomWrapper"
          style={{ height: onStatMode ? "4em" : "" }}
        >
          {deleteMode ? (
            <div
              className="bookListDeleteButton"
              onClick={handleDeleteMode}
              style={{ padding: onStatMode ? "1em 1em 0 1em" : "" }}
            >
              <img
                style={{ height: "1.15em", margin: "0 0.25em 0 0" }}
                src={
                  darkMode
                    ? "./src/assets/darkmode/done.svg"
                    : "./src/assets/done.svg"
                }
              />
              삭제 완료
            </div>
          ) : (
            <div
              className="bookListDeleteButton"
              onClick={handleDeleteMode}
              style={{
                padding: onStatMode ? "1em 1em 0 1em" : "",
                pointerEvents: onEditMode ? "none" : "auto",
              }}
            >
              <img
                style={{ height: "1.15em", margin: "0 0.25em 0 0" }}
                src={
                  darkMode
                    ? "./src/assets/darkmode/trash.svg"
                    : "./src/assets/trash.svg"
                }
              />
              선택 삭제
            </div>
          )}

          {onStatMode ? (
            <div
              className="bookListDeleteButton"
              onClick={handleStatMode}
              style={{ padding: onStatMode ? "1em 1em 0 1em" : "" }}
            >
              <img
                style={{ height: "1.15em", margin: "0 0.25em 0 0" }}
                src={
                  darkMode
                    ? "./src/assets/darkmode/arrowDown.svg"
                    : "./src/assets/arrowDown.svg"
                }
              />
              숨기기
            </div>
          ) : (
            <div
              className="bookListDeleteButton"
              onClick={handleStatMode}
              style={{ padding: onStatMode ? "1em 1em 0 1em" : "" }}
            >
              <img
                style={{ height: "1.15em", margin: "0 0.25em 0 0" }}
                src={
                  darkMode
                    ? "./src/assets/darkmode/arrowUp.svg"
                    : "./src/assets/arrowUp.svg"
                }
              />
              설정 및 통계
            </div>
          )}
        </div>
        <div
          className="bookListStat"
          style={{
            display: "flex",
            flexDirection: "row",
            height: onStatMode ? "11em" : "0",
            opacity: onStatMode ? "1" : "0",
          }}
        >
          <div className="bookListStatBackground">
            <div
              style={{
                display: "flex",
                flexDirection: "row",
                height: onStatMode ? "6.75em" : "0",
              }}
            >
              <div
                style={{
                  color: "var(--highlight-color)",
                  lineHeight: "1.5em",
                  margin: "0 1em 0 0",
                }}
              >
                ·&nbsp;&nbsp;&nbsp;등록된 책 권수
                <br />
                ·&nbsp;&nbsp;&nbsp;완독한 책 권수
                <br />
                ·&nbsp;&nbsp;&nbsp;평균 부여 평점
                <br />
                ·&nbsp;&nbsp;&nbsp;최고 평점 도서
              </div>
              <div
                style={{
                  color: "var(--primary-text-color)",
                  lineHeight: "1.5em",
                  margin: "0 1em 0 0",
                }}
              >
                {count}
                <br />
                {completeCount}
                <br />
                {(averageRating / 20).toFixed(2)}
                <br />
                {(maxRating / 20).toFixed(2)} ({maxRatingName})
              </div>
            </div>
            <div className="darkModeButton" onClick={handleDarkMode}>
              {darkMode ? (
                <>
                  <img
                    src="./src/assets/sun.svg"
                    style={{ height: "1em", margin: "0 0.5em 0 0" }}
                  ></img>
                  라이트 모드
                </>
              ) : (
                <>
                  <img
                    src="./src/assets/moon.svg"
                    style={{ height: "1em", margin: "0 0.5em 0 0" }}
                  ></img>
                  다크 모드
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default memo(BookListTitle);
