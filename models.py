from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

# Helper para manejar ObjectId en MongoDB
class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

# Modelo de Usuario
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "customer"  # Puede ser "customer" o "admin"

class UserResponse(BaseModel):
    id: PyObjectId
    name: str
    email: EmailStr
    role: str

    class Config:
        json_encoders = {ObjectId: str}


# Modelo para la solicitud de login (LoginRequest)
class LoginRequest(BaseModel):
    username: str
    password: str

# Modelo para la respuesta de login (LoginResponse)
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"  # Usualmente se usa "bearer" para el tipo de token
    name: str


# Modelo de Cliente
class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    user_id: Optional[str] = None

class ClientResponse(ClientCreate):
    id: PyObjectId
    pedidos: int = 0
    gasto_total: float = 0.0

    class Config:
        json_encoders = {ObjectId: str}


# Modelo de Producto
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    price_sale: Optional[float] = None
    type_product: str
    type_stock: bool
    stock: Optional[int] = None
    category: Optional[str] = None
    code_sku: Optional[str] = None
    code_bar: Optional[str] = None
    width: Optional[float] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    length: Optional[float] = None
    user_id: Optional[str] = None
    image_url: Optional[str] = None
class ProductResponse(ProductCreate):
    id: PyObjectId

    class Config:
        json_encoders = {ObjectId: str}


# Modelo de Pedido (Order)
class OrderItemCreate(BaseModel):
    product_id: PyObjectId
    quantity: int
    price: float
    name: str
    image_url: Optional[str] = None 
    

class OrderCreate(BaseModel):
    user_id: Optional[str] = None
    client_id: PyObjectId
    client_name: str
    total: float
    valor: float
    products: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: PyObjectId
    user_id: PyObjectId
    client_id: PyObjectId
    client_name: str
    total: float
    valor: float
    date: datetime  # Nuevo campo para la fecha
    products: List[OrderItemCreate]

    class Config:
           json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
