import BookListItem from "./BookListItem";
import BookListTitle from "./BookListTitle";
import { useState } from "react";

function BookList({ count, books, onDeleteBooks, setAnimationHeight }) {
  const [deleteMode, setDeleteMode] = useState(false);

  const handleDeleteMode = () => {
    setDeleteMode(deleteMode === true ? false : true);
    console.log(deleteMode);
  };

  return (
    <>
      <div className="bookList">
        <BookListTitle
          count={count}
          onDeleteMode={handleDeleteMode}
          deleteMode={deleteMode}
        />
        <BookListItem
          books={books}
          deleteMode={deleteMode}
          onDeleteBooks={onDeleteBooks}
          setAnimationHeight={setAnimationHeight}
        />
      </div>
    </>
  );
}

export default BookList;
