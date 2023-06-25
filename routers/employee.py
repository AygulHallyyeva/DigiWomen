from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from models import baseSchema
from db import get_db
import crud
from models.models import Employee


employee_router = APIRouter()


@employee_router.post('/add-employee')
def add_employee(req: baseSchema, db: Session = Depends(get_db)):
    try:
        result = crud.create_crud(req,Employee, db)
        if result:
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={'result': 'Successfully sign up!'})
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Something went wrong!!!')


@employee_router.get('/get-employee')
def get_employee( db: Session = Depends(get_db)):
    try:
        result = crud.read_employee(db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something went wrong!!!')


@employee_router.delete('/delete-employee/{id}')
def delete_employee(id: int, db: Session = Depends(get_db)):
    try:
        result = crud.delete_employee(id, db)
        return JSONResponse(status_code=status.HTTP_200_OK, content={'result': 'Successfully deleted!!!'})
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something went wrong!!!')    


@employee_router.get('/search-employee')
def search_employee(q: str, db: Session = Depends(get_db)):
    try:
        result = crud.search_employee(q,db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something went wrong!!!')   
    
    
    