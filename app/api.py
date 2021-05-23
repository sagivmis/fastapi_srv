import csv

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

import motor.motor_asyncio
from bson import ObjectId
import os

from .models import OrderModel, ProductModel, UpdateProductModel


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

products = [
    # {
    #   "id": 1,
    #   "text": "T-shirt",
    #   "price": 12,
    #   "description": "T-shirt",
    #   "show_description": False,
    #   "image": True,
    #   "reminder": False,
    #   "url":
    #     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnwBh410RwBSiaCOnUjohBG-WRrZjsAtv0BzZ5s-CYFyQUUEcmAYHw03jX8Nz012Gh39LF7Pr1&usqp=CAc",
    #   "quantity": 1,
    # },
    # {
    #   "id": 2,
    #   "text": "Shoes",
    #   "price": 50,
    #   "description": "Fun shoes",
    #   "show_description": False,
    #   "image": True,
    #   "reminder": False,
    #   "url": "https://sc04.alicdn.com/kf/HTB1rQWtXo6FK1Jjy0Foq6xHqVXaa.jpg",
    #   "quantity": 1,
    # },
    # {
    #   "id": 3,
    #   "text": "Coat",
    #   "price": 120,
    #   "description": "Beatiful",
    #   "show_description": False,
    #   "image": True,
    #   "reminder": False,
    #   "url":
    #     "https://i5.walmartimages.com/asr/b8591192-d5ae-46d2-ae5d-48ac793bf4c1.295f980b310499033ed8a7fdc4dc3e57.jpeg?odnWidth=612&odnHeight=612&odnBg=ffffff",
    #   "quantity": 0,
    # },
]

orders = [
    {
        "id": 1,
        "date": "2021-05-14",
        "total": 255,
        "item_ids": [1, 2, 3],
        "quantity": {"1": 1,
                     "2": 1,
                     "3": 1},

    }
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

### DB

MONGO_URL = os.getenv('MONGO_URL',
                      'mongodb+srv://admin:Sn59595959@cluster0.t7aoo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

database = client.whist

products_collection = database.get_collection('products')
orders_collection = database.get_collection('orders')

# ROUTES

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your shop."}

#ORDERS
@app.post('/orders', tags=['orders'])
async def add_order(order: OrderModel = Body(...)):
    try:
        new_order = await db_add_order(order=dict(order))
        return ResponseModel(new_order, 'Order added successfully.')
    except Exception as e:
        return ErrorResponseModel(error=e.__str__(), code=505, message='An error occurred.')


@app.get("/orders/{id}", tags=['orders'])
async def get_order(id):
    try:
        order = await db_get_order(id)
        if order:
            return ResponseModel(order, "Order data retrieved successfully")
        else:
            return ErrorResponseModel("An error occurred.", 404, "Order doesn'exist.")
    except Exception as e:
        return ErrorResponseModel(error=e.__str__(), code=505, message='An error occurred.')


@app.patch("/orders/{id}", tags=['orders'])
async def edit_order(id: str, order: OrderModel = Body(...)):
    try:
        updated_product = await db_edit_order(id, dict(order))
        return ResponseModel(updated_product, f'Order with ID: {id} name update is successful')
    except Exception as e:
        return ErrorResponseModel(error=e.__str__(), code=505, message='An error occurred.')


@app.get("/orders", tags=['orders'])
async def get_orders():
    try:
        orders = await db_get_orders()
        return ResponseModel(orders, 'Products')
    except Exception as e:
        return ErrorResponseModel(error=e.__str__(), code=505, message='An error occurred.')


@app.delete("/orders/{id}", tags=['orders'])
async def delete_order(id):
    try:
        is_deleted = await db_delete_order(id)
        if is_deleted:
            return ResponseEmptyModel("Order deleted successfully")
        else:
            return ErrorResponseModel("An error occurred.", 404, "Order doesn'exist.")
    except Exception as e:
        return ErrorResponseModel(error=e.__str__(), code=505, message='An error occurred.')


### PRODUCT SECTION

# FUNCTIONS
def product_helper(product):
    return {
        '_id': str(product['_id']),
        'text': product['text'],
        'price': product['price'],
        'description': product['description'],
        'show_description': product['show_description'],
        'image': product['image'],
        'reminder': product['reminder'],
        'url': product['url'],
        'quantity': product['quantity'],
    }


async def db_add_product(product):
    product = await products_collection.insert_one(product)
    new_product = await products_collection.find_one({'_id': product.inserted_id})
    return product_helper(new_product)


async def db_get_products():
    products = []
    async for product in products_collection.find():
        products.append(product_helper(product))
    return products


async def db_get_product(id):
    product = await products_collection.find_one({"_id": ObjectId(id)})
    if product:
        return product_helper(product)


async def db_delete_product(id):
    product = await products_collection.find_one({"_id": ObjectId(id)})
    if product:
        await products_collection.delete_one({"_id": ObjectId(id)})
        return True


async def db_edit_product(id, product):
    products_collection.update_one({"_id": ObjectId(id)}, {"$set": product})
    updated_product = await products_collection.find_one({"_id": ObjectId(id)})
    return product_helper(updated_product)


# ROUTES
@app.post('/products', tags=['products'])
async def add_product(product: ProductModel = Body(...)):
    try:
        new_product = await db_add_product(product=dict(product))
        return ResponseModel(new_product, 'Product added successfully.')
    except Exception as e:
        return ErrorResponseModel(error=e.__str__(), code=505, message='An error occurred.')


@app.patch("/products/{id}", tags=['products'])
async def edit_product(id: str, product: ProductModel = Body(...)):
    try:
        updated_product = await db_edit_product(id, dict(product))
        return ResponseModel(updated_product, f'Product with ID: {id} name update is successful')
    except Exception as e:
        return ErrorResponseModel(error=e.__str__(), code=505, message='An error occurred.')


@app.get("/products/{id}", tags=['products'])
async def get_product(id):
    try:
        product = await db_get_product(id)
        if product:
            return ResponseModel(product, "Product data retrieved successfully")
        else:
            return ErrorResponseModel("An error occurred.", 404, "Product doesn'exist.")
    except Exception as e:
        return ErrorResponseModel(error=e.__str__(), code=505, message='An error occurred.')


@app.delete("/products/{id}", tags=['products'])
async def delete_product(id):
    try:
        is_deleted = await db_delete_product(id)
        if is_deleted:
            return ResponseEmptyModel("Product deleted successfully")
        else:
            return ErrorResponseModel("An error occurred.", 404, "Product doesn'exist.")
    except Exception as e:
        return ErrorResponseModel(error=e.__str__(), code=505, message='An error occurred.')


@app.get("/products", tags=['products'])
async def get_products():
    try:
        products = await db_get_products()
        return ResponseModel(products, 'Products')
    except Exception as e:
        return ErrorResponseModel(error=e.__str__(), code=505, message='An error occurred.')


### ORDERS SECTION

# FUNCTIONS

def order_helper(order):
    return {
        '_id': str(order['_id']),
        'date': order['date'],
        'total': order['total'],
        'quantity': order['quantity'],
        'item_ids': order['item_ids'],
    }


async def db_add_order(order):
    order = await orders_collection.insert_one(order)
    new_order = await orders_collection.find_one({'_id': order.inserted_id})
    return order_helper(new_order)


async def db_delete_order(id):
    order = await orders_collection.find_one({"_id": ObjectId(id)})
    if order:
        await orders_collection.delete_one({"_id": ObjectId(id)})
        return True


async def db_edit_order(id, order):
    orders_collection.update_one({"_id": ObjectId(id)}, {"$set": order})
    updated_order = await orders_collection.find_one({"_id": ObjectId(id)})
    return order_helper(updated_order)


async def db_get_order(id):
    order = await orders_collection.find_one({"_id": ObjectId(id)})
    if order:
        return order_helper(order)


async def db_get_orders():
    orders = []
    async for order in orders_collection.find():
        orders.append(order_helper(order))
    return orders


### RESPONSE MODELS
def ResponseEmptyModel(message):
    return {
        "code": 200,
        "message": message,
    }


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }


"""
EXAMPLE OF ADD/UPDATE PRODUCT
{
"text":"T-shirt",
"price": 511,
"description": "Fun T",
"showDescription": false,
"image": true,
"reminder": false,
"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnwBh410RwBSiaCOnUjohBG-WRrZjsAtv0BzZ5s-CYFyQUUEcmAYHw03jX8Nz012Gh39LF7Pr1&usqp=CAc",
"quantity": 1
}
"""

"""
EXAMPLE OF ADD/UPDATE ORDER
{
"date": "2021-05-14",
"total": 255,
"item_ids": [1,2,3],
"quantity": {"1": 1,
"2": 1,
"3": 1},
}
"""
