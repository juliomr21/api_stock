# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from routes import router

# app = FastAPI()

# # Definir los orígenes permitidos
# origins = [
#     "http://localhost:4200",  # Para el entorno de desarrollo en local
#     "http://127.0.0.1:4200",  # Otra variante para local
#     "https://juliomr21.github.io/ecommerce-template"  # URL de producción del frontend
# ]

# # Agregar el middleware de CORS
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=origins,  # Permitir estas URLs
# #     allow_credentials=True,
# #     allow_methods=["*"],  # Permitir todos los métodos HTTP
# #     allow_headers=["*"],  # Permitir todos los headers
# # )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Acepta todos los orígenes
#     allow_credentials=True,
#     allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
#     allow_headers=["*"],  # Permitir todos los encabezados
# )

# # Incluir las rutas del API
# app.include_router(router)

# @app.get("/")
# async def root():
#     return {"message": "API de eCommerce con FastAPI y MongoDB"}


from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# Conexión a la base de datos
client = AsyncIOMotorClient("mongodb+srv://juliomr21correo:1yw0eZzoJiRFVuxn@cluster0.pcse6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["stock_db"]

@app.on_event("startup")
async def startup_db():
    try:
        # Verifica la conexión de MongoDB al inicio de la aplicación
        await db.command("ping")
        print("Conexión a MongoDB exitosa.")
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")

@app.get("/")
async def root():
    return {"message": "Aplicación en funcionamiento"}
