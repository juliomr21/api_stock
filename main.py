from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

app = FastAPI()

origins = [
    "http://localhost:4200",  # Angular en desarrollo
    "http://127.0.0.1:4200",  # Otra variante
    "https://juliomr21.github.io"
]

# Agregar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir estas URLs
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permitir todos los headers
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "API de eCommerce con FastAPI y MongoDB"}