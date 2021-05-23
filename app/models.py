from pydantic import BaseModel, Field
from typing import Optional

### MODELS
class OrderModel(BaseModel):
    date: str = Field(...)
    total: int = Field(...)
    quantity: list = Field(...)
    item_ids: list = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "products": [
                    {
                        "date": "12-31-1994",
                        "total": 250,
                        "quantity": [1, 1, 1],
                        "item_ids": [1, 2, 3]
                    },
                ]
            }
        }


class ProductModel(BaseModel):
    _id: int = Field(...)
    text: str = Field(...)
    price: int = Field(...)
    description: str = Field(...)
    show_description: bool = Field(...)
    image: bool = Field(...)
    reminder: bool = Field(...)
    url: str = Field(...)
    quantity: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "text": "T-shirt",
                "price": 12,
                "description": "T-shirt",
                "showDescription": False,
                "image": True,
                "reminder": False,
                "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnwBh410RwBSiaCOnUjohBG-WRrZjsAtv0BzZ5s-CYFyQUUEcmAYHw03jX8Nz012Gh39LF7Pr1&usqp=CAc",
                "quantity": 1
            }
        }


class UpdateProductModel(BaseModel):
    _id: Optional[int]
    text: Optional[str]
    price: Optional[int]
    description: Optional[str]
    show_description: Optional[bool]
    image: Optional[bool]
    reminder: Optional[bool]
    url: Optional[str]
    quantity: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "text": "Flowery T-shirt",
                "price": 12,
                "description": "T-shirt with flower patterns",
                "showDescription": False,
                "image": True,
                "reminder": False,
                "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnwBh410RwBSiaCOnUjohBG-WRrZjsAtv0BzZ5s-CYFyQUUEcmAYHw03jX8Nz012Gh39LF7Pr1&usqp=CAc",
                "quantity": 1
            }
        }
