from random import Random

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from src.FastApiCrashCourse.database import DBManager
from env_loader import EnvLoader
from src.FastApiCrashCourse.product.models import Product
from src.FastApiCrashCourse.product.database_models import Product as OrmProduct

EnvLoader.initializeEnvs()
db_manager = DBManager()
app = FastAPI()
rand = Random()

@app.get("/")
def greet(name: str):
    return { 'word': f'Welcome to FastAPI! {name}'}

# def generate_random_products():
#     products = []
#     for x in range(rand.randint(a=10, b=1000)):
#         product = Product(
#             id=x,
#             name=f"Product {x * rand.randint(a=0, b=100)}",
#             description=f"Description {x * rand.randint(a=0, b=100)}",
#             price=rand.uniform(a=1.0, b=100.9),
#             quantity=rand.randint(a=0, b=100)
#         )
#         products.append(product)
#     return products
#
# CURRENT_PRODUCTS = generate_random_products()

@app.get("/products")
# inject the db session
def get_all_products(db: Session = Depends(db_manager.get_db_session)):
    products_from_db = db.query(OrmProduct).all()
    return products_from_db

@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(db_manager.get_db_session)):
    try:
        result = db.query(OrmProduct).filter(OrmProduct.id == id).first()
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
def add_product(product: Product, db: Session = Depends(db_manager.get_db_session)):
    try:
        db.add(OrmProduct(**product.model_dump()))
        db.commit()
        return product
    except Exception as ex:
        print(f"Exception: {ex}")
        raise HTTPException(status_code=500, detail="Something went wrong")

@app.delete("/product/{id}")
def delete_product(id: int, db: Session = Depends(db_manager.get_db_session)):
    try:
        product = db.query(OrmProduct).filter(OrmProduct.id == id).first()
        if product is not None:
            db.delete(product)
            db.commit()
            return Product(**product.model_dump())
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except Exception as ex:
        print(f"Exception: {ex}")
        raise HTTPException(status_code=500, detail="Something went wrong")