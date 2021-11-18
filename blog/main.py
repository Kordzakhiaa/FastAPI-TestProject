from fastapi import FastAPI, status
from schemas import Blog

app = FastAPI()


@app.get('/', status_code=status.HTTP_200_OK)
def index():
    return {'message': 'index page', 'status': 200}


@app.post('/create', status_code=status.HTTP_201_CREATED)
def create(request: Blog):
    return {'data': request, 'status': 201}
