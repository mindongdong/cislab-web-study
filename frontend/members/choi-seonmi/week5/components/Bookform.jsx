
const Bookform = ({form, setFormData, onClickAddButton, inputFocus, theme}) => {

  const onChange = (e) => {
    setFormData({
        ...form,
        [e.target.name]: e.target.value
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    onClickAddButton();
  }

  console.log(form)
  return (
    <div className={`Bookform Bookform-${theme}`}>
      <h3> ✎ &nbsp; 읽은 책을 기록해주세요</h3>
      <form onSubmit={handleSubmit}>
        <div className='info'>
          <div>
            <p>제목 🕮</p>
            <input className={`input-info input-info-${theme}`}
              ref={inputFocus} 
              name="title"
              value={form.title}
              onChange={onChange}
              placeholder='책의 제목을 입력해주세요'
            />
          </div>
          <div>
            <p>저자 &nbsp;⍩</p>
            <input className={`input-info input-info-${theme}`}
              name="author"
              value={form.author}
              onChange={onChange}
              placeholder='저자의 이름을 입력해주세요'
            />
          </div>
        </div>

        <div>
          <p>별점 ⋆⁺₊⋆</p>
          <div>
            <input type='radio' name='star' id='option1' value='1' onChange={onChange} checked={form.star === '1'} />
            <label for="option1">❶&nbsp;&nbsp;</label>
            <input type='radio' name='star' id='option2' value='2' onChange={onChange} checked={form.star === '2'} />
            <label for="option2">❷&nbsp;&nbsp;</label>
            <input type='radio' name='star' id='option3' value='3' onChange={onChange} checked={form.star === '3'} />
            <label for="option3">❸&nbsp;&nbsp;</label>
            <input type='radio' name='star' id='option4' value='4' onChange={onChange} checked={form.star === '4'} />
            <label for="option4">❹&nbsp;&nbsp;</label>
            <input type='radio' name='star' id='option5' value='5' onChange={onChange} checked={form.star === '5'} />
            <label for="option5">❺&nbsp;&nbsp;</label>
          </div>
        </div>

        <div>
          <p>메모 ❏</p>
          <textarea className={`textarea textarea-${theme}`} name="memo" value={form.memo} onChange={onChange}
          rows='8' cols='40'/>
        </div>

        <div>
          <button type="submit" className={`button-add button-add-${theme}`}><i class="fa-solid fa-plus"></i></button>
        </div>
      </form>
    </div>
  );
};

export default Bookform;
