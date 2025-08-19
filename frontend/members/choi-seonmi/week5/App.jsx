import './App.css'
import Bookform from './components/Bookform'
import Bookitem from './components/Bookitem'

import { useState, useRef } from 'react'

function App() {

  const [books, setBooks] = useState([])
  const [form, setFormData] = useState({
    title: '',
    author: '',
    star: '3',
    memo: ''
  })

  const inputFocus = useRef(null);

  const onClickAddButton = () => {
    if (!form.title) return;

    const addBook = {
      id: Date.now(),
      title: form.title,
      author: form.author,
      star: form.star,
      memo: form.memo
    }

    setBooks([...books, addBook])
    setFormData({
      title: '',
      author: '',
      star: 0,
      memo: ''
    })

    inputFocus.current.focus();
    

  }

  const onClickDelButton = (id) => {

    setBooks(books.filter(book => book.id !== id));

  }

  const [theme, setTheme] = useState('light')
  const changeTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light')
  }

  return (
    <div className={`container container-${theme}`}>
    <div className='App'>
      <div class='Headers'>
        <h1> ⟪ 간단 독서기록장 ⟫ </h1>
        <button className='button-mode' onClick={changeTheme}> 
          {theme === 'light' ? '☀︎' : <i class="fa-solid fa-moon"></i> } 
          </button>
      </div>

      <div className={`section section-${theme}`}>
        <Bookform form={form} setFormData={setFormData} onClickAddButton={onClickAddButton} inputFocus={inputFocus} theme={theme}/>
      </div>
      
      <div className={`section section-${theme}`}>
        <Bookitem books={books} onClickDelButton={onClickDelButton} theme={theme}/>
      </div>

    </div>
    </div>
  )
}

export default App
