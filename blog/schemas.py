from pydantic import BaseModel, EmailStr


class Blog(BaseModel):
    title: str
    body: str


class ShowBlog(Blog):
    """ Schema that inherits Blog and shows title and body in view (response_model) """

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    email: EmailStr
    password: str


class ShowUser(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
