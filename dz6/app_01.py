# Урок 6. Дополнительные возможности FastAPI
# Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц: товары, заказы и пользователи.
# — Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
# — Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
# — Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
# • Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия,
# адрес электронной почты и пароль.
# • Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
# • Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.
#
# Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц.
# Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API.
from datetime import datetime
from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field

DATABASE_URL = "sqlite:///DZ/dz6/my_database2.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("surname", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(32)),
)

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(128)),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("price", sqlalchemy.Float),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), index=True),
    sqlalchemy.Column("product_id", sqlalchemy.ForeignKey("products.id"), index=True),
    sqlalchemy.Column("order_date", sqlalchemy.DateTime),
    sqlalchemy.Column("status", sqlalchemy.String(32)),
)
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(max_length=32)


class User(BaseModel):
    id: int
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(max_length=32)


class ProductIn(BaseModel):
    name: str = Field(max_length=128)
    description: str
    price: float


class Product(BaseModel):
    id: int
    name: str = Field(max_length=128)
    description: str
    price: float


class OrderIn(BaseModel):
    user_id: int
    product_id: int
    status: str = Field(max_length=32)


class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: datetime
    status: str = Field(max_length=32)


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name, surname=user.surname, email=user.email, password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(name=new_user.name, surname=new_user.surname,
                                                               email=new_user.email, password=new_user.password)
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


@app.post("/products/", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(name=product.name, description=product.description, price=product.price)
    last_record_id = await database.execute(query)
    return {**product.dict(), "id": last_record_id}


@app.get("/products/", response_model=List[Product])
async def read_products():
    query = products.select()
    return await database.fetch_all(query)


@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(
        name=new_product.name, description=new_product.description, price=new_product.price
    )
    await database.execute(query)
    return {**new_product.dict(), "id": product_id}


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {'message': 'Product deleted'}


@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(
        user_id=order.user_id, product_id=order.product_id, order_date=datetime.now(), status=order.status
    )
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}


@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(
        user_id=new_order.user_id, product_id=new_order.product_id, status=new_order.status
    )
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}
