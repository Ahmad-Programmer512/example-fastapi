from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated

class NoteSchema(BaseModel):
    title: str
    content: str

class UserSchema(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    id: int

    class Config:
        from_attributes = True

class NoteResponse(NoteSchema):
    id: int
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    note_id: int
    dir: Annotated[int, Field(ge=0, le=1)]