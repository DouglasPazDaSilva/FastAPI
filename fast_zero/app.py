from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fast_zero.routers.auth import router as auth
from fast_zero.routers.todos import router as todos
from fast_zero.routers.users import router as users


app = FastAPI()

app.include_router(users)
app.include_router(auth)
app.include_router(todos)

app.middleware('http')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def read_root():
    return {'message': 'Olar Mundo!'}
