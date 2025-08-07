import './App.css'
import Bookform from './components/Bookform'
import Bookitem from './components/Bookitem'

import { useState, useRef } from 'react'

function App() {

  const [books, setBooks] = useState([])
  const [form, setFormData] = useState({
    title: '',
    author: '',
    star: 0,
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

  return (
    <div className='App'>
      <h1> ⟪ 간단 독서기록장 ⟫ </h1>

      <section>
        <Bookform form={form} setFormData={setFormData} onClickAddButton={onClickAddButton} inputFocus={inputFocus}/>
      </section>
      
      <section>
        <Bookitem books={books} onClickDelButton={onClickDelButton}/>
      </section>

    </div>
  )
}

export default App
