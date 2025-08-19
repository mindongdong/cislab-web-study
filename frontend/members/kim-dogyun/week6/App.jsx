import "./stylesheets/App.css";
import BookList from "./components/BookList";
import BookForm from "./components/BookForm";
import {
  useState,
  useEffect,
  useRef,
  useReducer,
  useCallback,
  useMemo,
  createContext,
} from "react";

function bookReducer(state, action) {
  switch (action.type) {
    case "SET":
      return JSON.parse(action.data);

    case "ADD":
      return [action.data, ...state];

    case "DELETE":
      return state.filter((book) => book.id !== action.data);

    case "EDIT":
      return state.map((book) => {
        if (book.id === action.data.id) {
          return { ...book, ...action.data };
        } else {
          return book;
        }
      });

    default:
      return state;
  }
}

export const DataStateContext = createContext();
export const DataSetContext = createContext();
export const ThemeStateContext = createContext();
export const ThemeSetContext = createContext();

function App() {
  const [books, dispatchBooks] = useReducer(bookReducer, []);
  // const [books, setBooks] = useState([]);
  const [isAdding, setIsAdding] = useState(0);
  const [animationHeight, setAnimationHeight] = useState(0);
  const [search, setSearch] = useState("");
  const [searchMode, setSearchMode] = useState("none");
  const [darkMode, setDarkMode] = useState(false);
  const [onStatMode, setOnStatMode] = useState(false);
  const [onEditMode, setOnEditMode] = useState(false);
  const [editBook, setEditBook] = useState({});
  const [deleteMode, setDeleteMode] = useState(false);
  const [clickedBookItem, setClickedBookItem] = useState(0);
  const [atTop, setAtTop] = useState(true);

  const isFirstDarkModeRender = useRef(true);
  const isFirstBooksRender = useRef(true);
  const isFirstAnimationRender = useRef(true);
  const Animation = useRef();

  useEffect(() => {
    if (isFirstDarkModeRender.current) {
      isFirstDarkModeRender.current = false;
      const data = localStorage.getItem("darkMode");
      if (JSON.parse(data) == true) {
        setDarkMode(true);
        document.documentElement.setAttribute("color-theme", "dark");
      } else {
        setDarkMode(false);
        document.documentElement.setAttribute("color-theme", "light");
      }
    } else {
      darkMode
        ? document.documentElement.setAttribute("color-theme", "dark")
        : document.documentElement.setAttribute("color-theme", "light");
      localStorage.setItem("darkMode", JSON.stringify(darkMode));
    }
  }, [darkMode]);

  useEffect(() => {
    if (isFirstBooksRender.current) {
      isFirstBooksRender.current = false;
      const data = localStorage.getItem("books");
      if (data) {
        dispatchBooks({
          type: "SET",
          data: data,
        });
      } else {
        localStorage.setItem("books", JSON.stringify(books));
      }
      return;
    }
    localStorage.setItem("books", JSON.stringify(books));
  }, [books]);

  useEffect(() => {
    if (isFirstAnimationRender.current) {
      isFirstAnimationRender.current = false;
      return;
    }
    const anim = Animation.current;
    anim.style.transition = "none";
    if (onEditMode) {
      anim.style.opacity = "0";
      anim.style.transform = "scale(0)";
      anim.style.marginRight = "55%";
      anim.style.top = `${clickedBookItem.top * 2 - 700}px`;
      console.log("EditEnter");
      requestAnimationFrame(() => {
        anim.style.transition = "";
        anim.style.opacity = "1";
        anim.style.transform = "scale(1)";
        anim.style.marginRight = "0";
        anim.style.top = `170px`;
      });

      setTimeout(() => {
        anim.style.opacity = "0";
      }, 400);
    } else {
      requestAnimationFrame(() => {
        anim.style.transition =
          "opacity 0.1s cubic-bezier(0.97, 0.01, 0.89, 0.41),transform 0.9s cubic-bezier(0.63, 0.04, 0, 0.99),margin-right 0.9s cubic-bezier(0.63, 0.04, 0, 0.99),top 0.9s cubic-bezier(0.63, 0.04, 0, 0.99), background-color 0.3s";
        anim.style.opacity = "1";
        anim.style.transform = "scale(0)";
        anim.style.marginRight = "55%";
        anim.style.top = `${clickedBookItem.top * 2 - 700}px`;
        setTimeout(() => {
          anim.style.opacity = "0";
        }, 300);
      });
    }
    // eslint-disable-next-line
  }, [onEditMode]);

  const handleAddBook = useCallback((newBook) => {
    dispatchBooks({
      type: "ADD",
      data: {
        id: Date.now(),
        name: newBook.name,
        author: newBook.author,
        rating: newBook.rating,
        review: newBook.review,
        liked: newBook.liked,
        status: newBook.status,
        hidden: newBook.hidden,
      },
    });

    // 책 추가 시 애니메이션
    setIsAdding(1);
    setTimeout(() => {
      setIsAdding(2);
    }, 400);
  }, []);

  const handleDeleteBook = useCallback((deleteBook) => {
    dispatchBooks({
      type: "DELETE",
      data: deleteBook.id,
    });
    // 책 삭제 시 애니메이션은 bookItem에서 자체적으로 실행
  }, []);

  const handleEditBook = useCallback((editBook) => {
    dispatchBooks({
      type: "EDIT",
      data: editBook,
    });

    // 책 편집 시 오작동 방지 레이어 활성화 및 애니메이션
    setOnEditMode(false);
  }, []);

  const themeState = { darkMode };

  const themeSet = useMemo(() => {
    return { setDarkMode };
  });

  const dataState = {
    books,
    search,
    searchMode,
    onStatMode,
    editBook,
    onEditMode,
    deleteMode,
    atTop,
  };

  const dataSet = useMemo(() => {
    return {
      handleAddBook,
      handleEditBook,
      handleDeleteBook,
      setAnimationHeight,
      setSearch,
      setSearchMode,
      setOnStatMode,
      setOnEditMode,
      setEditBook,
      setDeleteMode,
      setClickedBookItem,
      setAtTop,
    };
  }, []);

  return (
    <>
      <div className="background" style={{ overflow: "hidden" }}>
        <div style={{ overflow: "hidden" }}>
          <div ref={Animation} className="bookEditAnimation"></div>
          <div
            className={`bookAnimation ${isAdding == 1 ? "isAdding" : ""}${
              isAdding == 2 ? "isAddingFinished" : ""
            }`}
            style={{
              transform:
                isAdding === 1
                  ? !atTop
                    ? "scale(0)"
                    : searchMode === "none"
                    ? "scaleX(0.15) scaleY(0.05)"
                    : "scale(0)"
                  : "scale(1)",
              bottom:
                isAdding == 1
                  ? `calc(${!atTop ? -100 : -animationHeight - 115}px + 72.5%)`
                  : "",
            }}
          ></div>
        </div>
        <div className="bookBlocker">
          <div
            className={`bookListBlocker ${onEditMode ? "active" : ""}`}
          ></div>
          <div
            className={`bookFormBlocker ${
              (searchMode !== "none" || deleteMode) && !onEditMode
                ? "active"
                : ""
            }`}
          ></div>
        </div>

        <ThemeStateContext.Provider value={themeState}>
          <ThemeSetContext.Provider value={themeSet}>
            <DataStateContext.Provider value={dataState}>
              <DataSetContext.Provider value={dataSet}>
                <BookList />
                <BookForm />
              </DataSetContext.Provider>
            </DataStateContext.Provider>
          </ThemeSetContext.Provider>
        </ThemeStateContext.Provider>
      </div>
    </>
  );
}

export default App;
