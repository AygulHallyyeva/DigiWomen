from fastapi import FastAPI
from db import Base, engine
from routers import employee_router, image_router, authentication_router

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(authentication_router, tags=['Authentication'])
app.include_router(employee_router, tags=['Employees'])
app.include_router(image_router, tags=['Images'])