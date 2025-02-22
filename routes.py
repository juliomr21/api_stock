from typing import List
from fastapi import APIRouter, HTTPException, Depends
from database import db
from models import LoginRequest, LoginResponse, UserCreate, UserResponse, ClientCreate, ClientResponse, ProductCreate, ProductResponse, OrderCreate, OrderResponse
from auth import get_current_user, hash_password, verify_password, create_access_token
from bson import ObjectId

router = APIRouter()

# Colecciones de MongoDB
users_collection = db["users"]
clients_collection = db["clients"]
products_collection = db["products"]
orders_collection = db["orders"]

# Ruta para crear un usuario
@router.post("/users", response_model=LoginResponse)
async def create_user(user: UserCreate):
    # Convertir el usuario a un diccionario y encriptar la contraseña
    user_dict = user.dict()
    user_dict["password"] = hash_password(user_dict["password"])
    
    # Insertar el nuevo usuario en la base de datos
    result = await users_collection.insert_one(user_dict)

    # Generar el token de acceso, utilizando el ID insertado
    access_token = create_access_token(user_id=str(result.inserted_id))
    
    # Recuperar el nombre del usuario recién creado
    user_name = user_dict.get("name")

    # Retornar la respuesta similar a la de login
    return LoginResponse(access_token=access_token, name=user_name)


# Ruta para hacer login
@router.post("/login", response_model=LoginResponse)
async def login_for_access_token(form_data: LoginRequest):
    # Buscar el usuario por su nombre de usuario (email o username)
    user = await users_collection.find_one({"email": form_data.username})
    if user is None or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # Crear el token de acceso con el ID del usuario
    access_token = create_access_token(user_id=str(user["_id"]))  # Pasar el ID en vez del email
    
    return LoginResponse(access_token=access_token, name=user["name"])

# Ruta para obtener información del usuario usando el token


@router.get("/users/me", response_model=UserResponse)
async def get_current_user_info(current_user: str = Depends(get_current_user)):
    # Obtener el usuario por ID en vez de email
    current_user_id = ObjectId(current_user) if isinstance(current_user, str) else current_user
    print('id:', current_user_id)
    print('Tipo de current_user_id:', type(current_user_id))  # Imprime el tipo de objeto
    
    user = await users_collection.find_one({"_id": current_user_id})
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado vvv")
    
    user["id"] = user["_id"]
    del user["_id"]  # Eliminar el campo _id, ya que 'id' es lo que queremos devolver

    return user

# Ruta para obtener un usuario por ID
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["id"] = str(user["_id"])
        return user
    raise HTTPException(status_code=404, detail="User not found")

# Crear un cliente
@router.post("/clients", response_model=ClientResponse)
async def create_client(client: ClientCreate,current_user: str = Depends(get_current_user)):
    client_data = client.dict()
    client_data["user_id"] = current_user

    result = await db["clients"].insert_one(client_data)
    return ClientResponse(id=str(result.inserted_id), **client_data)

# Obtener todos los clientes
@router.get("/clients", response_model=List[ClientResponse])
async def get_clients(current_user: str = Depends(get_current_user)):
    # Filtrar los clientes por el ID del usuario actual
    clients = await db["clients"].find({"user_id": current_user}).to_list(100)

    # Si no se encuentran clientes, retornar una respuesta vacía o lanzar una excepción si es necesario
    if not clients:
        raise HTTPException(status_code=404, detail="No se encontraron clientes para este usuario")

    # Mapear los clientes y retornar la respuesta
    return [ClientResponse(id=str(client["_id"]), **client) for client in clients]
# Crear un producto
@router.post("/products", response_model=ProductResponse)
async def create_product(product: ProductCreate):
    product_data = product.dict()
    result = await db["products"].insert_one(product_data)
    return ProductResponse(id=str(result.inserted_id), **product_data)

# Obtener todos los productos
@router.get("/products", response_model=List[ProductResponse])
async def get_products():
    products = await db["products"].find().to_list(100)
    return [ProductResponse(id=str(product["_id"]), **product) for product in products]

# Obtener un producto por su id
@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product_by_id(product_id: str):
    # Convertir el id a ObjectId de MongoDB
    product_object_id = ObjectId(product_id)
    
    # Buscar el producto en la base de datos
    product = await db["products"].find_one({"_id": product_object_id})
    
    # Si no se encuentra el producto, lanzar un error 404
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Devolver el producto encontrado
    return ProductResponse(id=str(product["_id"]), **product)

# Actualizar un producto por su id
@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product: ProductCreate):
    # Convertir el id a ObjectId de MongoDB
    product_object_id = ObjectId(product_id)    
    # Buscar el producto en la base de datos
    existing_product = await db["products"].find_one({"_id": product_object_id})    
    # Si no se encuentra el producto, lanzar un error 404
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")    
    # Convertir los datos del producto a un diccionario
    product_data = product.dict()
    # Actualizar el producto en la base de datos
    update_result = await db["products"].update_one(
        {"_id": product_object_id}, {"$set": product_data}
    )

    # Si no se actualizó ningún documento, lanzar un error
    if update_result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el producto")
    
    # Obtener el producto actualizado
    updated_product = await db["products"].find_one({"_id": product_object_id})
    
    # Devolver el producto actualizado
    return ProductResponse(id=str(updated_product["_id"]), **updated_product)

# Eliminar un producto por su id
@router.delete("/products/{product_id}", response_model=ProductResponse)
async def delete_product(product_id: str):
    # Convertir el id a ObjectId de MongoDB
    product_object_id = ObjectId(product_id)
    
    # Buscar el producto en la base de datos
    existing_product = await db["products"].find_one({"_id": product_object_id})
    
    # Si no se encuentra el producto, lanzar un error 404
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Eliminar el producto de la base de datos
    delete_result = await db["products"].delete_one({"_id": product_object_id})
    
    # Si no se eliminó ningún documento, lanzar un error
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=400, detail="No se pudo eliminar el producto")
    
    # Devolver el producto eliminado
    return ProductResponse(id=str(existing_product["_id"]), **existing_product)

# Crear un pedido
@router.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate):
    order_data = order.dict()
    result = await db["orders"].insert_one(order_data)
    return OrderResponse(id=str(result.inserted_id), **order_data)

# Obtener todos los pedidos
@router.get("/orders", response_model=List[OrderResponse])
async def get_orders():
    orders = await db["orders"].find().to_list(100)
    return [OrderResponse(id=str(order["_id"]), **order) for order in orders]