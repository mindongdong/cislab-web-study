from pydantic import BaseModel, StringConstraints, ConfigDict
from typing import Annotated, List
from datetime import datetime,date

a_str = Annotated[str, StringConstraints(max_length=200)]
b_str = Annotated[str,StringConstraints(max_length=100)]
c_str = Annotated[str,StringConstraints(max_length=50)]
d_str = Annotated[str,StringConstraints(max_length=13)]

class BookModel(BaseModel):
    id : int
    title : a_str #200
    author : b_str #100
    isbn : d_str #13
    price : int
    stock_quantity : int
    published_date : date | None
    created_at : datetime
    updated_at : datetime
    category_id : int
    
    model_config = ConfigDict(from_attributes=True)
    
class CategoryModel(BaseModel):
    id : int
    name : c_str #50
    description: str
    created_at : datetime
    
    model_config = ConfigDict(from_attributes=True)
    

class ListBookModel(BookModel):
    Book : List[BookModel]
    
    
    