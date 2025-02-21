from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_URI = 'mongodb+srv://juliomr21correo:1yw0eZzoJiRFVuxn@cluster0.pcse6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = AsyncIOMotorClient(MONGO_URI)
db = client["stock_db"]
