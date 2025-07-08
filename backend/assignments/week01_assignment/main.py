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
    # TODO: 게시판 모델 구현
    board_id: int

class Post(BaseModel):
    # TODO: 게시글 모델 구현
    post_id: int
    board_id: int
    user_id: int
    title: str
    content: str

class PostCreate(BaseModel):
    # TODO: 게시글 생성용 모델 구현
    board_id: int
    user_id: Optional[int] = None
    title: str
    content: str

mock_users = [
    User(user_id=1, username="alice", email="alice@example.com"),
    User(user_id=2, username="bob", email="bob@example.com"),
    User(user_id=3, username="charlie", email="charlie@example.com")
]

mock_boards = [
    Board(board_id=1),
    Board(board_id=2),
    Board(board_id=3)
]

mock_posts = [
    Post(post_id=1, board_id=1, user_id=1, title="첫 번째 게시글", content="첫 번째 게시글 내용"),
    Post(post_id=2, board_id=1, user_id=2, title="두 번째 게시글", content="두 번째 게시글 내용"),
    Post(post_id=3, board_id=2, user_id=1, title="세 번째 게시글", content="세 번째 게시글 내용")
]

app = FastAPI()

@app.get("/boards")
def get_boards():
    return mock_boards


@app.get("/boards/{bid}")
def get_board(bid: int):
    return Board(board_id=bid)
    
@app.get("/boards/{bid}/posts")
def get_posts(bid: int):
    result = []
    for post in mock_posts:
        if post.board_id == bid:
            result.append(post)
    return result
    
@app.get("/posts/{pid}")
def get_post(pid: int):
    for post in mock_posts:
        if post.post_id == pid:
            return post
    
@app.post("/posts")
def create_post(post: PostCreate):
    if post.user_id is None:
        post.user_id = max(user.user_id for user in mock_users) + 1
    new_post = Post(
        post_id = len(mock_posts) + 1,
        board_id = post.board_id,
        user_id = post.user_id,
        title = post.title,
        content = post.content
    )
    mock_posts.append(new_post)