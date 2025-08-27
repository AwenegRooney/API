from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import Optional

app = FastAPI()

class Product(BaseModel):
    id : Optional[UUID] = uuid4()
    name : str
    price : int

class Order(BaseModel):
    order_id: Optional[UUID] = uuid4()
    product_id : UUID
    quantity : int

products = [
    Product(
        id=uuid4(), name='Pen', price=100
    ),
    Product(
        id=uuid4(), name='Bag', price=3000
    ),
    Product(
        id=uuid4(), name='Book', price=350
    )
]

orders = [
    Order(
        order_id=uuid4(), product_id=products[0].id, quantity=50
    ), 
    Order(
        order_id=uuid4(), product_id=products[2].id, quantity=10
    )
]

@app.get('/')
def display_products():
    return {"Available": products}

@app.post('/products/add')
def add_product(new_product: Product):
    for product in products:
        if product.name.lower() == new_product.name.lower():
            raise HTTPException(
                status_code=409, 
                detail=f"{new_product.name.capitalize()} already exist exist."
            )
    new_product.id = uuid4()
    products.append(new_product)
    return f"{new_product.name.capitalize()} was added"

@app.delete('/products/remove/{product_id}')
def remove_order(product_id: UUID):
    for product in products:
        if product.id == product_id:
            products.remove(product)
            return f"Product {product_id} removed"
        
    raise HTTPException(
        status_code=404,
        detail=f"Product with id {product_id}, doesn't exist."
    )

@app.get('/orders')
def display_orders():
    return {"Orders": orders}

@app.post('/orders/add')
def add_order(order: Order):
    for product in products:
        if product.id == order.product_id:
            order.order_id = uuid4()
            orders.append(order)
            return {"Name": product.name, "Quantity": order.quantity}
        
    raise HTTPException(
        status_code=404, 
        detail=f"Product with id {order.product_id} doesn't exist."
    )

@app.delete('/orders/delete/{order_id}')
def remove_order(order_id: UUID):
    for order in orders:
        if order.order_id == order_id:
            orders.remove(order)
            return f"Order {order_id} removed"
        
    raise HTTPException(
        status_code=404,
        detail=f"Order with id {order_id}, doesn't exist."
    )