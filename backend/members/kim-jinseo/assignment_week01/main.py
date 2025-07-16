from fastapi import FastAPI, Query, Path , HTTPException
from pydantic import BaseModel,Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

# 이미 구현되어 있다고 가정하는 User 모델
class User(BaseModel):
    user_id: int
    username: str
    email: str

# 여러분이 구현해야 할 모델들
class Board(BaseModel):
    board_id:int
    name : str
    description : Optional[str]=None
    create_time : datetime
    

class Post(BaseModel):
    post_id : int
    board_id : int
    user_id : int
    title : str
    content: Optional[str] = None
    create_time : datetime
    reference : Optional[List[str]]=Field(default_factory=list)
    

class PostCreate(BaseModel):
    board_id:int
    title : str
    content : Optional[str] =None
    reference : Optional[List[str]]=Field(default_factory=list)
    
#목업 데이터: 사용자
mock_users = [
    User(user_id=1, username="제갈권", email="제갈권@example.com"),
    User(user_id=2, username="허가온", email="허가온@example.com"),
    User(user_id=3, username="김주찬", email="김주찬@example.com"),
    User(user_id=4, username="김진서", email="김진서@example.com")
]

#목업데이터 : 게시판
# TODO: 최소 3개 이상의 게시판 목업 데이터 작성
mock_boards = [
    Board(board_id=1, name='마음의 편지', description='누가 괴롭히나요?', create_time=datetime.now() ),
    Board(board_id=2, name='선임의 편지', description='내가 괴롭혔나요?', create_time=datetime.now()),
    Board(board_id=3,  name='행사 일정표', description='행사 일정을 공지합니다', create_time=datetime.now() ),
    Board(board_id=4,  name='작업 일정표', description='작업 일정을 공지합다', create_time=datetime.now() ),
    Board(board_id=5,  name='짬표',        description='누가 전역 하나요?', create_time=datetime.now() )
    
    # 예시: Board(board_id=1, ...)
]

mock_posts = [
    Post(post_id=1, board_id=1, user_id=1, title="병장 김진서를 고발합니다.",  content="자꾸 취침시간 전에 춤을 추게 합니다.", create_time=datetime.now()),
    Post(post_id=2, board_id=1, user_id=1, title="상병 김진서를 고발합니다.",  content="훈련할때 너무 가혹합니다.", create_time=datetime.now()),
    Post(post_id=3, board_id=1, user_id=2, title="병장 김진서 전역 안하나요?", content="취침시간에 자고 싶은데 자꾸 옆에 누워서 놀아달라고 말겁니다.", create_time=datetime.now()),
    Post(post_id=4, board_id=2, user_id=4, title="억울합니다.",                content="전 때리진 않았잖아요.", create_time=datetime.now()),
    Post(post_id=5, board_id=2, user_id=4, title="요즘 군대가 군대냐?",        content="요즘 애들 빠졌다;;", create_time=datetime.now()),
    Post(post_id=6, board_id=3, user_id=3, title="10.1 국군의 날 행사",        content="병장 김진서 등 15명", create_time=datetime.now()),
    Post(post_id=7, board_id=4, user_id=3, title="7/1제초작업",                content="풀 뽑으세요.", create_time=datetime.now()),
    Post(post_id=8, board_id=5, user_id=3, title="7/10 제초작업",              content="풀이 또 자랐습니다.", create_time=datetime.now()),
]


app = FastAPI()

#모든 게시판 조회
@app.get("/boards")
def get_boards():
    return mock_boards

#특정 게시판 조회
@app.get("/boards/{board_id}")
def get_board(board_id: int=Path(...,gt=0)):
    board = next((i for i in mock_boards if i.board_id == board_id), None)
    if board is None:
        raise HTTPException(404, "Board not found")
    return board


#목록 조회(게시판, 키워드)
@app.get("/boards/{board_id}/posts")
def get_posts(board_id: int=Path(...,gt=0), keyword:Optional[str] =Query(None, min_length=2), limit:int=Query(1,ge=1,le=100)):
    posts = [i for i in mock_posts if i.board_id == board_id]
    if keyword:
        posts = [j for j in posts if keyword.lower() in j.title.lower()]
    return posts[:limit]


#특정 게시글 조회
@app.get("/posts/{post_id}")
def get_post(post_id: int = Path(..., gt=0)):
    post = next((j for j in mock_posts if j.post_id == post_id), None)
    if post is None:
        raise HTTPException(404, "Post not found")
    return post


#게시글 작성
@app.post("/posts", status_code=201)
def create_post(post: PostCreate):
    new_id = max(i.post_id for i in mock_posts) + 1
    new_post = Post(
        post_id=new_id,
        board_id=post.board_id,
        user_id=1,                       
        title=post.title,
        content=post.content,
        reference=post.reference or [],   
        create_time=datetime.now()
    )
    mock_posts.append(new_post)
    return new_post


    