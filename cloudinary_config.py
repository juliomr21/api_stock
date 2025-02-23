import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from cloudinary import config as cloudinary_config
from dotenv import load_dotenv

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Configurar Cloudinary con las credenciales del entorno
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
   

)
