from random import Random

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from src.FastApiCrashCourse.database import DBManager
from env_loader import EnvLoader
from src.FastApiCrashCourse.product.models import Product, ProductCreate
from src.FastApiCrashCourse.product.database_models import Product as OrmProduct

EnvLoader.initializeEnvs()
db_manager = DBManager()
app = FastAPI()
rand = Random()

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
def add_product(product: ProductCreate, db: Session = Depends(db_manager.get_db_session)):
    try:
        orm_product = OrmProduct(**product.model_dump())
        db.add(orm_product)
        db.commit()
        db.refresh(orm_product)
        return orm_product
    except Exception as ex:
        print(f"Exception: {ex}")
        raise HTTPException(status_code=500, detail="Something went wrong")

@app.delete("/product/{id}")
def delete_product(id: int, db: Session = Depends(db_manager.get_db_session)):
    try:
        product = db.query(OrmProduct).filter(OrmProduct.id == id).first()
        if product is not None:
            result = Product.model_validate(product, from_attributes=True)
            db.delete(product)
            db.commit()
            return result
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except Exception as ex:
        print(f"Exception: {ex}")
        raise HTTPException(status_code=500, detail="Something went wrong")