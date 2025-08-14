import "./../stylesheets/BookList.css";
import BookListItem from "./BookListItem";
import BookListTitle from "./BookListTitle";
import { useState, memo, createContext } from "react";

export const SearchContext = createContext();

function BookList() {
  const [searchRating, setSearchRating] = useState(0);
  const [searchStatus, setSearchStatus] = useState("all");

  const searchState = {
    searchRating,
    setSearchRating,
    searchStatus,
    setSearchStatus,
  };

  return (
    <>
      <SearchContext.Provider value={searchState}>
        <div className="bookList">
          <BookListTitle />
          <BookListItem />
        </div>
      </SearchContext.Provider>
    </>
  );
}

export default memo(BookList);
