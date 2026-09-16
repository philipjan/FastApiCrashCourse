from contextlib import asynccontextmanager
from random import Random

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from env_loader import EnvLoader
from src.FastApiCrashCourse.database import Base
from src.FastApiCrashCourse.database import DBManager
from src.FastApiCrashCourse.product.database_models import Product as OrmProduct
from src.FastApiCrashCourse.product.models import Product, ProductCreate

EnvLoader.initializeEnvs()
db_manager = DBManager()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup
    async with db_manager.db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await db_manager.db_engine.dispose()

app = FastAPI(lifespan=lifespan)
rand = Random()

@app.get("/products")
# inject the db session
async def get_all_products(db: AsyncSession = Depends(db_manager.get_db_session)):
    products_from_db = await db.execute(select(OrmProduct))
    return products_from_db.scalars().all()

@app.get("/product/{id}")
async def get_product_by_id(id: int, db: AsyncSession = Depends(db_manager.get_db_session)):
    try:
        result = await db.execute(select(OrmProduct).where(OrmProduct.id == id))
        db_product = result.scalars().first()
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        else:
            return db_product
    except IndexError:
        raise HTTPException(status_code=404, detail="Product not found")
    except HTTPException as ex:
        raise ex
    except Exception as ex:
        print(f"Exception: {ex}")
        raise HTTPException(status_code=500, detail="Something went wrong")

@app.post("/product")
async def add_product(product: ProductCreate, db: AsyncSession = Depends(db_manager.get_db_session)):
    try:
        user_from_db = await db.execute(select(OrmProduct).where(OrmProduct.name == product.name))
        existing_user = user_from_db.scalars().first()
        if existing_user:
            raise HTTPException(status_code=409, detail="Product already exists")
        else:
            new_product = OrmProduct(**product.model_dump())
            db.add(new_product)
            await db.commit()
            await db.refresh(new_product)
            return new_product
    except HTTPException as ex:
        raise ex
    except Exception as ex:
        print(f"Exception: {ex}")
        raise HTTPException(status_code=500, detail="Something went wrong")

@app.put("/product")
async def update_product(product: Product, db: AsyncSession = Depends(db_manager.get_db_session)):
    try:
        existing_product = await db.execute(select(OrmProduct).where(OrmProduct.id == product.id))
        db_product = existing_product.scalars().first()
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        else:
            db_product.name = product.name
            db_product.description = product.description
            db_product.price = product.price
            db_product.quantity = product.quantity
            await db.commit()
            await db.refresh(db_product)
            return db_product
    except HTTPException as ex:
        raise ex
    except Exception as ex:
        print(f"Exception: {ex}")
        raise HTTPException(status_code=500, detail="Something went wrong")


@app.delete("/product/{id}")
async def delete_product(id: int, db: AsyncSession = Depends(db_manager.get_db_session)):
    try:
        result = await db.execute(select(OrmProduct).where(OrmProduct.id == id))
        db_product = result.scalars().first()
        if db_product is not None:
            await db.delete(db_product)
            await db.commit()
            return db_product
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except HTTPException as ex:
        raise ex
    except Exception as ex:
        print(f"Exception: {ex}")
        raise HTTPException(status_code=500, detail="Something went wrong")