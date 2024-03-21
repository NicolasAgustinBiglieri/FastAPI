from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/products",
                   tags=["products"],
                   responses={404: {"message": "No encontrado"}})

# Entidad product
class Product(BaseModel):
    id: int
    name: str

products_list = [Product(id=1, name="Product_1"),
                 Product(id=2, name="Product_2"),
                 Product(id=3, name="Product_3")]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def product(id: int):
    products = filter(lambda product: product.id == id, products_list)
    try:
        return list(products)[0]
    except:
        raise HTTPException(status_code=404, detail="Producto inexistente")
