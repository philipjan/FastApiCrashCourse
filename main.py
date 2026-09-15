from random import Random

from fastapi import FastAPI, HTTPException

from src.FastApiCrashCourse.product.models import Product

app = FastAPI()
rand = Random()

@app.get("/")
def greet(name: str):
    return { 'word': f'Welcome to FastAPI! {name}'}

def generate_random_products():
    products = []
    for x in range(rand.randint(a=10, b=1000)):
        product = Product(
            id=x,
            name=f"Product {x * rand.randint(a=0, b=100)}",
            description=f"Description {x * rand.randint(a=0, b=100)}",
            price=rand.uniform(a=1.0, b=100.9),
            quantity=rand.randint(a=0, b=100)
        )
        products.append(product)
    return products

CURRENT_PRODUCTS = generate_random_products()

@app.get("/products")
def get_all_products():
    return CURRENT_PRODUCTS

@app.get("/product/{id}")
def get_product_by_id(id: int):
    try:
        result = next((x for x in CURRENT_PRODUCTS if x.id == id), None)
        if result is None:
            raise HTTPException(status_code=404, detail="Product not found")
        else:
            return result
    except IndexError:
        raise HTTPException(status_code=404, detail="Product not found")
    except HTTPException as ex:
        raise ex
    except Exception as ex:
        print(f"Exception: {ex}")
        raise HTTPException(status_code=500, detail="Something went wrong")

@app.post("/product")
def add_product(product: Product):
    try:
        result = next((x for x in CURRENT_PRODUCTS if x.id == product.id), None)
        if result is None:
            CURRENT_PRODUCTS.append(product)
            return product
        else:
            CURRENT_PRODUCTS[product.id] = product
            return product
    except Exception as ex:
        print(f"Exception: {ex}")
        raise HTTPException(status_code=500, detail="Something went wrong")

@app.delete("/product/{id}")
def delete_product(id: int):
    try:
        result = next((x for x in CURRENT_PRODUCTS if x.id == id), None)
        if result is None:
            raise HTTPException(status_code=404, detail="Product not found")
        else:
            CURRENT_PRODUCTS.remove(result)
            return result
    except HTTPException as ex:
        raise ex
    except Exception as ex:
        print(f"Exception: {ex}")
        raise HTTPException(status_code=500, detail="Something went wrong")