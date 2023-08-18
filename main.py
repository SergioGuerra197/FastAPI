from fastapi import FastAPI, Body, Path, Query, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List
from starlette.requests import Request
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer


app = FastAPI()  # Instancia de fastAPI
app.title = "Mi aplicación con fastAPI" #Modificacion titulo de la documentacion
app.version = "0.0.1"#Modifica la version de la aplicacion, se refleja en la documentacion de swager

# gt: greater than
# ge: greater than or equal
# lt: less than
# le: less than or equal


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth= await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code=403, data = 'credenciales invalidas')

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] | None = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(default=2022,le=2022)
    rating: float = Field(ge=1,le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra= {
            'example':{
                'id':1,
                'title': 'Mi pelicula',
                'overview': 'Descripcion de la pelicula',
                'year': 2022,
                'rating': 8.9,
                'category': 'Accion'
            }
        }


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'El exorcismo del papa',
        'overview': "El padre Gabriele Amorth, exorcista personal del papa, es un hombre sencillo, divertido y práctico en ocasiones...",
        'year': '2023',
        'rating': 8.8,
        'category': 'Terror'    
    }
]


@app.get('/',tags = ['home'])
def message():
    return HTMLResponse('<h1>Hola mundo</H1>')


#Ruta que permite al usuario loguearse


@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict())
    return JSONResponse(status_code=200, content=token)


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

# @app.get('/movies', tags=['movies'])
# def get_movies():
#     return movies


@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie_by_id(id : int = Path(ge=1,le=2000)) -> Movie:
    for item in movies: 
        if item['id'] == id:
            return  JSONResponse(content=item)
    return  JSONResponse(status_code=404, content=[])

# @app.get('/movies/{id}', tags=['movies'])
# def get_movie_by_id(id : int = Path(ge=1,le=2000)):
#     for item in movies:
#         if item['id'] == id:
#             return  item
#     return  'No se encontro la pelicula'




#Parametros Query son parametros clave valor, si no especifico el parametro en la ruta FastAPI va a requerir una variable Query
# @app.get('/movies/', tags=['movies'])
# def get_movies_by_category(categoria: str = Query(min_length=5, max_length=15)):   
#     return [item for item in movies if ['category'] == categoria ]

@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(categoria: str = Query(min_length=5, max_length=15)) -> List[Movie]:  
    data = [item for item in movies if ['category'] == categoria ]
    return JSONResponse(content=data)


# @app.post('/movies', tags=['movies'])
# def create_movie(id : int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
#     movies.append({
#         "id": id,
#         "title": title,
#         "overview": overview,
#         "year": year,
#         "rating": rating,
#         "category": category        
#     })
#     return title

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie : Movie)-> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={'message':'Se registró la pelicula'})



# @app.put('/movies/{id}', tags=["movies"])
# def update_movie(id : int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
#     for item in movies:
#         if item['id'] == id:
#             item['title'] = title,
#             item['overview'] = overview,
#             item['year'] = year,
#             item['rating'] = rating,
#             item['category'] = category
#             return movies
        
@app.put('/movies/{id}', tags=["movies"],response_model=dict, status_code=200)
def update_movie(id : int, movie: Movie) -> dict :
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(status_code=200,content={'message':'Se ha actualizado la pelicula'})
            
            


@app.delete('/movies/{id}', tags=['movies'],response_model=dict, status_code=200)
def delete_movie(id: int) -> dict :
    for item in movies:
        if item['id'] == id:
           movies.remove(item)
           return JSONResponse(status_code=200, content={'message':'Se ha eliminado la pelicula'})
        
