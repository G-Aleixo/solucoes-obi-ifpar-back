from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import dependencies
from . import database
database.Base.metadata.create_all(database.engine)
from . import auth

app = FastAPI()
app.include_router(auth.router)


origins = [
    "http://localhost:5000",
    "http://localhost:5173",
    "https://g-aleixo.github.io",
    "https://solucoes-obi-ifpar.onrender.com",
    "https://clubeppar.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return "root!"

@app.get("/admin")
def admin_panel(admin: auth.AdminDep):
    return [admin["username"], admin["id"]]