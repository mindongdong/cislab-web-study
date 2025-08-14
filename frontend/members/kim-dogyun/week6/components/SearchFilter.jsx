import "./../stylesheets/SearchFilter.css";
import { memo, useContext } from "react";
import { DataSetContext, DataStateContext } from "../App";
import { SearchContext } from "./BookList";

function SearchFilter() {
  const { search, searchMode, onEditMode } = useContext(DataStateContext);
  const { setSearch, setSearchMode } = useContext(DataSetContext);
  const { searchRating, setSearchRating, searchStatus, setSearchStatus } =
    useContext(SearchContext);

  const onChangeSearch = (e) => {
    setSearch(e.target.value);
  };

  const onChangeSearchMode = (e) => {
    setSearchMode(e.target.value);
    setSearch("");
    setSearchRating("all");
    setSearchStatus("all");
  };

  const onChangeSearchRating = (e) => {
    setSearchRating(e.target.value);
  };

  const onChangeSearchStatus = (e) => {
    setSearchStatus(e.target.value);
  };

  return (
    <div className="bookListTitleSearch">
      <div
        className="bookListTitleSearchWrapper"
        style={{ pointerEvents: onEditMode ? "none" : "auto" }}
      >
        <select onChange={onChangeSearchMode}>
          <option value="none">모두 표시</option>
          <option value="name">제목</option>
          <option value="author">작가</option>
          <option value="rating">별점</option>
          <option value="status">완독 여부</option>
          <option value="liked">즐겨찾기</option>
        </select>
        {searchMode === "none" ? (
          ""
        ) : searchMode === "liked" ? (
          ""
        ) : searchMode === "rating" ? (
          <select value={searchRating} onChange={onChangeSearchRating}>
            <option value="all">모든 별점</option>
            <option value="5">★★★★★ (완벽 5점)</option>
            <option value="4">★★★★☆ (4점대)</option>
            <option value="3">★★★☆ (3점대)</option>
            <option value="2">★★☆ (2점대)</option>
            <option value="1">★☆ (1점대)</option>
            <option value="0">☆ (한 개 주기도 아까움) &nbsp;</option>
          </select>
        ) : searchMode === "status" ? (
          <select value={searchStatus} onChange={onChangeSearchStatus}>
            <option value="all">모든 상태</option>
            <option value="2">완독</option>
            <option value="1">읽는 중</option>
            <option value="0">읽을 예정</option>
          </select>
        ) : (
          <input
            value={search}
            onChange={onChangeSearch}
            placeholder="여기에 검색어를 입력하세요"
          ></input>
        )}
      </div>
    </div>
  );
}

export default memo(SearchFilter);
