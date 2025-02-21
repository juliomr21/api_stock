from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

app = FastAPI()

# Definir los orígenes permitidos
origins = [
    "http://localhost:4200",  # Para el entorno de desarrollo en local
    "http://127.0.0.1:4200",  # Otra variante para local
    "https://juliomr21.github.io/ecommerce-template"  # URL de producción del frontend
]

# Agregar el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir estas URLs
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los headers
)

# Incluir las rutas del API
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "API de eCommerce con FastAPI y MongoDB"}
