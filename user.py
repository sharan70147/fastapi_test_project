# models.py

from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from markdown_it.rules_block import table
from sqlmodel import Field, Session, SQLModel, create_engine, select
from starlette import schemas


class UserBase(SQLModel):
    email = str = Field(nullable=False ,unique=True)
    password = str = Field(nullable=False)
    # created_at = datetime=Field(timezone=True,nullable=)

class User(UserBase,table=True):
    id: int | None = Field(default=None, primary_key=True)

sqlite_file_name = "user_data.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)
def create_db_and_tables():
   SQLModel.metadata.create_all(engine)


def get_session():
   with Session(engine) as session:
      yield session

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()

@app.post("/users/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserBase, db: SessionDep ):
    # Hash the password here (discussed later)
    new_user = User.model_validate(user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user