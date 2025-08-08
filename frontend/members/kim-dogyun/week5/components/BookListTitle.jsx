function BookListTitle({ count, onDeleteMode, deleteMode }) {
  return (
    <>
      <div className="bookListTitle">
        <div className="bookListTitleLogo">
          <div className="lobster-regular">BookBook</div>
          <img src="./src/assets/bookbook.svg" />
        </div>
        <div className="bookListTitleCount">저장한 책: {count}</div>
        <div className="bookListTitleBackground"></div>
        <div className="bookListTitleBackgroundBlur"></div>
      </div>
      <div className="bookListTitleBottom">
        {deleteMode ? (
          <div className="bookListDeleteButton" onClick={onDeleteMode}>
            <img
              style={{ height: "1.15em", margin: "0 0.25em 0 0" }}
              src="./src/assets/done.svg"
            />
            완료
          </div>
        ) : (
          <div className="bookListDeleteButton" onClick={onDeleteMode}>
            <img
              style={{ height: "1.15em", margin: "0 0.25em 0 0" }}
              src="./src/assets/trash.svg"
            />
            선택 삭제
          </div>
        )}
      </div>
    </>
  );
}

export default BookListTitle;
