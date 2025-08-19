import './App.css'
import Bookform from './components/Bookform'
import Booklist from './components/Booklist'

import {  useRef, useEffect, useReducer, useCallback, createContext } from 'react'

const initialState = {
  books: [],
  form: {
    title: '',
    author: '',
    star: '3',
    memo: ''
  },
  theme: 'light'
}

const ACTIONS = {
  ADD_BOOK: 'ADD_BOOK',
  DELETE_BOOK: 'DELETE_BOOK',
  UPDATE_FORM: 'UPDATE_FORM',
  LOAD_BOOKS: 'LOAD_BOOKS',
  TOGGLE_FAVORITE: 'TOGGLE_FAVORITE',
  CHANGE_THEME: 'CHANGE_THEME'
}

function bookReducer(state, action) {
  switch (action.type) {
    case ACTIONS.ADD_BOOK:
      const newBook = {
        id: Date.now(),
        title: state.form.title,
        author: state.form.author,
        star: state.form.star,
        memo: state.form.memo,
        isFavorite: false
      }
      return {
        ...state,
        books: [...state.books, newBook],
        form: {
          title: '',
          author: '',
          star: '3',
          memo: ''
        }
      }

    case ACTIONS.DELETE_BOOK:
      return {
        ...state,
        books: state.books.filter(book => book.id !== action.payload)
      }

    case ACTIONS.UPDATE_FORM:
      return {
        ...state,
        form: {
          ...state.form,
          ...action.payload
        }
      }

    case ACTIONS.LOAD_BOOKS:
      return {
        ...state,
        books: action.payload
      }

    case ACTIONS.TOGGLE_FAVORITE:
      return {
        ...state,
        books: state.books.map(book =>
          book.id === action.payload
            ? { ...book, isFavorite: !book.isFavorite }
            : book
        )
      }


    case ACTIONS.CHANGE_THEME:
      return {
        ...state,
        theme: state.theme === 'light' ? 'dark' : 'light'
      }

    default:
      return state
  }
}

export const BookContext = createContext()
export const ThemeContext = createContext()

function App() {
  
  const [state, dispatch] = useReducer(bookReducer, initialState)
  const { books, form, theme } = state
  
  const inputFocus = useRef(null)

  const onClickAddButton = useCallback(() => {
    if (!form.title) return
    
    dispatch({ type: ACTIONS.ADD_BOOK })
    inputFocus.current.focus()
  }, [form])
  
  const onClickDelButton = useCallback((id) => {
    dispatch({ type: ACTIONS.DELETE_BOOK, payload: id })
  })

  const updateForm = useCallback((updates) => {
    dispatch({ type: ACTIONS.UPDATE_FORM, payload: updates })
  })

  const changeTheme = useCallback(() => {
    dispatch({ type: ACTIONS.CHANGE_THEME })
  })

  const toggleFavorite = useCallback((id) => {
    dispatch({ type: ACTIONS.TOGGLE_FAVORITE, payload: id })
  })

  useEffect(() => {
    const savedBooks = JSON.parse(localStorage.getItem('books'));
    if (savedBooks) {
      dispatch({ type: ACTIONS.LOAD_BOOKS, payload: savedBooks })
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('books', JSON.stringify(books));
  }, [books]);


  return (

    <ThemeContext.Provider value={{theme, changeTheme}}>
    <div className={`container container-${theme}`}>
    <div className='App'>
      <div className='Headers'>
        <h1> ⟪ 간단 독서기록장 ⟫ </h1>
        <button className='button-mode' onClick={changeTheme}> 
          {theme === 'light' ? '☀︎' : <i class="fa-solid fa-moon"></i> } 
          </button>
      </div>
      
      <BookContext.Provider
        value={{
          form,
          books,
          onClickAddButton,
          onClickDelButton,
          updateForm,
          inputFocus,
          toggleFavorite,
        }}  
      >
        <div className={`section section-${theme}`}>
          <Bookform />
        </div>

        <div className={`section section-${theme}`}>
          <Booklist />
        </div>
      </BookContext.Provider>
    </div>
    </div>
    </ThemeContext.Provider>
  )
}

export default App
