from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
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
    board_id: int
    boardname: str | None = None
    description: str | None = None

class Post(BaseModel):
    post_id: int
    board_id: int
    user_id: int
    title: str | None = None
    content: str | None = None
    created_at: datetime = datetime.now()
    views: int | None = None

class PostCreate(BaseModel):
    board_id:int
    title: str
    content: str | None = None

# ---

mock_users = [
    User(user_id=1, username="alice", email="alice@example.com"),
    User(user_id=2, username="bob", email="bob@example.com"),
    User(user_id=3, username="charlie", email="charlie@example.com")
]

mock_boards = [
    Board(board_id=1, boardname="자유게시판", description="자유롭게 이야기를 나눠보세요!"),
    Board(board_id=2, boardname="질문게시판", description="백엔드에 대해 질문해봐요!"),
    Board(board_id=3, boardname="공유게시판", description="백엔드 정보를 공유해봐요!")
]

mock_posts = [
    Post(post_id=1, board_id=1, user_id=1, title="첫 글"),
    Post(post_id=2, board_id=1, user_id=2, title="가입 인사 드립니다"),
    Post(post_id=3, board_id=1, user_id=3, title="안녕하세요 여러분"),
    Post(post_id=4, board_id=3, user_id=1, title="백엔드 기초 강의 정보 공유해요"),
    Post(post_id=5, board_id=2, user_id=2, title="엔드포인트가 뭐에요?"),
    Post(post_id=6, board_id=2, user_id=3, title="엔드포인트가 뭐냐면...")
]

app = FastAPI()

# 1. 게시판 관련 API

@app.get("/boards", response_model=List[Board])
def get_boards():
    """모든 게시판 목록을 조회합니다."""
    return mock_boards

@app.get("/boards/{board_id}", response_model=Board)
def get_board(
	board_id: int
):
    """특정 게시판 정보를 조회합니다."""
    for board in mock_boards:
        if board.board_id == board_id:
            return board
    # return board for board in


# 2. 게시글 관련 API

@app.get("/boards/{board_id}/posts")
def get_posts(
    board_id: int
):
    """특정 게시판의 게시글 목록을 조회합니다."""
    # TODO: 구현
    pass
    
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    """특정 게시글을 조회합니다."""
    # TODO: 구현
    pass

@app.post("/posts")
def create_post(
    new_post: PostCreate
):
    """새로운 게시글을 생성합니다."""
    # TODO: 구현
    pass

