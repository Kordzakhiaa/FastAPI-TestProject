from typing import List, Union, Tuple

from fastapi import FastAPI, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

import models
from hashing import Hash
from database import engine, SessionLocal
import schemas

models.Blog.metadata.create_all(engine)  # Creating all tables
models.User.metadata.create_all(engine)  # Creating all tables


def get_db():
    """ Function that gets database """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get('/', status_code=status.HTTP_200_OK)
def index():
    """ Index page """

    return {'message': 'index page'}


@app.post('blog/create/', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    """ View that creates blog """

    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return {'data': {'new_blog': new_blog}}


@app.get('blog/list/', status_code=status.HTTP_200_OK)
def blogs(db: Session = Depends(get_db)):
    """ View that lists all blogs """

    all_blogs = db.query(models.Blog).all()
    return {'all_blogs': all_blogs}


@app.get('/blog/{id}/', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog(id: int, db: Session = Depends(get_db)):
    """ View where you can get specific blog by id """

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {id} not found')
    return {'blog': blog}


@app.delete('/blog/delete/{id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    """ View which ensures the deletion of a specific blog """

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {id} not found and cannot be deleted')
    blog.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/blog/update/{id}/', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    """ View which provides update of a specific blog """

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {id} not found and cannot be updated')
    blog.update(request.dict())
    db.commit()

    return {'updated_blog': request}


@app.post('/user/register/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    """ View that provides new user creation """

    new_user = models.User(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/list', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def users(db: Session = Depends(get_db)):
    """ View that lists all Users """

    all_users = db.query(models.User).all()

    return all_users
