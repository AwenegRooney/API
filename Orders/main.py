from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional

app = FastAPI()

class Product(BaseModel):
    id : UUID = Field(default_factory=uuid4)
    name : str
    price : int

class ProductUpdate(BaseModel):
    name : str = None
    price : int = None

class Order(BaseModel):
    order_id: UUID = Field(default_factory=uuid4)
    product_id : UUID = Field(default_factory=uuid4)
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
def endpoints():
    return {
        "Health" : "Alive",
        "/products" : "List of available products",
        "/products/add" : "Add a new product",
        "/products/delete" : "Remove a specific product",
        "/products/update" : "Updates a product",
        "/orders" : "List of all orders",
        "/orders/add" : "Adding a new order",
        "/orders/delete" : "Remove a specific order"
    }

@app.get('/products')
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
    products.append(new_product)
    return {"Product_id": new_product.id, "status": "Added"}

@app.delete('/products/delete/{product_id}')
def remove_order(product_id: UUID):
    for product in products:
        if product.id == product_id:
            products.remove(product)
            return {"Product_id": product_id, "status": "Deleted"}
        
    raise HTTPException(
        status_code=404,
        detail=f"Product with id {product_id}, doesn't exist."
    )

@app.put('/products/update/{product_id}')
def update_product(product_id : UUID, update: ProductUpdate):
    if not update.name and not update.price:
        return {"Product_id": product_id, "Status": "No change"}
    
    #updating the product
    for product in products:
        if product.id == product_id:
            if update.name and update.name.lower() != product.name:
                for exist_products in products:
                    if exist_products.id != product_id and exist_products.name.lower() == update.name.lower():
                        raise HTTPException(
                            status_code=409,
                            detail=f"Product name '{update.name}' already exists."
                        )

                product.name = update.name

            if update.price:
                product.price = update.price
            return {"Product_id": product_id, "Status": "Updated"}
                

@app.get('/orders')
def display_orders():
    return {"Orders": orders}

@app.post('/orders/add')
def add_order(order: Order):
    for product in products:
        if product.id == order.product_id:
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
            return {"Order_id": order_id, "status": "Deleted"}
        
    raise HTTPException(
        status_code=404,
        detail=f"Order with id {order_id}, doesn't exist."
    )