from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, SessionLocal
from schemas import Blog

models.Blog.metadata.create_all(engine)  # Creating all tables


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get('/', status_code=status.HTTP_200_OK)
def index():
    return {'message': 'index page', 'status': 200}


@app.post('/create', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return {'data': {'new_blog': new_blog}}


@app.get('/all_blogs', status_code=status.HTTP_200_OK)
def blogs(db: Session = Depends(get_db)):
    all_blogs = db.query(models.Blog).all()

    return {'all_blogs': all_blogs}
