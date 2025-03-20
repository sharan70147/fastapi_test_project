from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, APIRouter
from markdown_it.rules_block import table
from sqlmodel import Field, Session, SQLModel, create_engine, select



class BooksBase(SQLModel):
   title: str = Field(index=True)
   author:str | None = Field(default=None, index=True)
   publisher: str

class BooksPublic(BooksBase):
   id: int

class Books(BooksBase,table=True):
   id: int | None = Field(default=None, primary_key=True)


mysql_url = "mysql+mysqlconnector://root/voice_agent"



engine = create_engine(mysql_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        session.expire_on_commit = False
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
   SQLModel.metadata.create_all(engine)


def get_session():
   with Session(engine) as session:
      yield session

# SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()

version_v1 = APIRouter()
version_v2 = APIRouter()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post('/book/add/',response_model=BooksPublic)
def create_book(b1: BooksBase, session : SessionDep):
   db_books = Books.model_validate(b1)
   session.add(db_books)
   session.commit()
   return db_books

@version_v1.get("/books/list/",response_model=list[BooksPublic])
def read_books(db: SessionDep,
               offset: int = 0,
               limit:Annotated[int, Query(l1=100)]=100,
):
   books = db.exec(select(Books).offset(offset).limit(limit)).all()
   return books

@version_v2.get("/book/{book_id}",response_model=BooksPublic)
def read_book(book_id:int, db:SessionDep):
   book = db.get(Books,book_id)
   if not book:
      raise HTTPException(status_code=404,detail="Book not found")
   return book

@app.delete("/book/{book_id}")
def delete_book(book_id:int,db:SessionDep):
   book = db.get(Books,book_id)
   if not book:
      raise HTTPException(status_code=404,detail="Book not found")
   db.delete(book)
   db.commit()
   return {
      "successful":"Book delete successfully"
   }

app.include_router(version_v1,prefix="/v1")
app.include_router(version_v2,prefix="/v2")