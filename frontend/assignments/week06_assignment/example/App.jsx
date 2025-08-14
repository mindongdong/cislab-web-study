import React from 'react';
import { BookProvider } from './context/BookContext';
import { ThemeProvider } from './context/ThemeContext';
import Header from './components/Header';
import SearchFilter from './components/SearchFilter';
import BookForm from './components/BookForm';
import BookList from './components/BookList';
import './App.css';

function App() {
  return (
    <ThemeProvider>
      <BookProvider>
        <div className="app">
          <div className="container">
            <Header />
            <main className="main-content">
              <SearchFilter />
              <BookForm />
              <BookList />
            </main>
            <footer className="footer">
              <p>© 2024 나의 독서 기록장 | React.js 고도화 실습</p>
            </footer>
          </div>
        </div>
      </BookProvider>
    </ThemeProvider>
  );
}

export default App;