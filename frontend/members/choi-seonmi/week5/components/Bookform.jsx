

const Bookform = ({form, setFormData, onClickAddButton, inputFocus}) => {

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
    <div className='Bookform'>
      <h3> ✎ &nbsp; 읽은 책을 기록해주세요</h3>
      <form onSubmit={handleSubmit}>
        <div className='info'>
          <div>
            <p>제목 🕮</p>
            <input ref={inputFocus} 
              name="title"
              value={form.title}
              onChange={onChange}
              className='input-info'
              placeholder='책의 제목을 입력해주세요'
            />
          </div>
          <div>
            <p>저자 &nbsp;⍩</p>
            <input
              name="author"
              value={form.author}
              onChange={onChange}
              className='input-info'
              placeholder='저자의 이름을 입력해주세요'
            />
          </div>
        </div>

        <div>
          <p>별점 ⋆⁺₊⋆</p>
          <div>
            <input type='radio' name='star' value='1' onChange={onChange} checked={form.star === '1'} />
            ❶&nbsp;&nbsp;
            <input type='radio' name='star' value='2' onChange={onChange} checked={form.star === '2'} />
            ❷&nbsp;&nbsp;
            <input type='radio' name='star' value='3' onChange={onChange} checked={form.star === '3'} />
            ❸&nbsp;&nbsp;
            <input type='radio' name='star' value='4' onChange={onChange} checked={form.star === '4'} />
            ❹&nbsp;&nbsp;
            <input type='radio' name='star' value='5' onChange={onChange} checked={form.star === '5'} />
            ❺
          </div>
        </div>

        <div>
          <p>메모 ❏</p>
          <textarea name="memo" value={form.memo} onChange={onChange}
          rows='8' cols='40'/>
        </div>

        <div>
          <button type="submit" className='button-add'>등록</button>
        </div>
      </form>
    </div>
  );
};

export default Bookform;
