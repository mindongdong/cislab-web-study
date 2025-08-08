import "./App.css";
import BookList from "./components/BookList";
import BookForm from "./components/BookForm";
import { useState } from "react";

function App() {
  const [books, setBooks] = useState([]);
  const [count, setCount] = useState(0);
  const [isAdding, setIsAdding] = useState(0);
  const [animationHeight, setAnimationHeight] = useState(0);

  const handleAddBook = (props) => {
    const newBook = {
      id: Date.now(),
      name: props.name,
      author: props.author,
      rating: props.rating,
      review: props.review,
    };

    setBooks([...books, newBook]);
    setCount(count + 1);
    setIsAdding(1);
    console.log(animationHeight);

    setTimeout(() => {
      setIsAdding(2);
    }, 400);
  };

  const handleDeleteBook = (props) => {
    setBooks(books.filter((element) => element.id !== props.id));
    setCount(count - 1);
    console.log(books);
  };

  return (
    <>
      <div className="background" style={{ overflow: "hidden" }}>
        <div style={{ overflow: "hidden" }}>
          <div
            className={`bookAnimation ${isAdding == 1 ? "isAdding" : ""}${
              isAdding == 2 ? "isAddingFinished" : ""
            }`}
            style={{
              transform:
                isAdding === 1
                  ? animationHeight > document.body.clientHeight - 100
                    ? "scale(0)"
                    : "scaleX(0.15) scaleY(0.05)"
                  : "scale(1)",
              bottom:
                isAdding == 1
                  ? `calc(${
                      animationHeight > document.body.clientHeight - 100
                        ? -document.body.clientHeight
                        : -animationHeight - 25
                    }px ${books.length > 1 ? "+ 72.5%" : "+ 72.5%"})`
                  : "",
            }}
          ></div>
        </div>
        <BookList
          books={books}
          count={count}
          onDeleteBooks={handleDeleteBook}
          setAnimationHeight={setAnimationHeight}
        />
        <BookForm onAddBook={handleAddBook} animationHeight={animationHeight} />
      </div>
    </>
  );
}

export default App;
