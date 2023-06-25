from fastapi import APIRouter, Depends, status, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db import get_db
import crud
from models import employeeImages

image_router = APIRouter()

@image_router.post('/upload-employee-img')
def upload_employee_img(id: int, db: Session = Depends(get_db), file: UploadFile = File(...)):
    try:
        result = crud.create_employee_image(id, file, db)
        result = jsonable_encoder(result)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something went wrong!!!')


@image_router.delete('/delete-employee-image/{id}')
def delete_employee_image(id: int, db: Session = Depends(get_db)):
    try:
        result = db.query(employeeImages).filter(employeeImages.id == id)\
            .delete(synchronize_session=False)
        db.commit()
        return JSONResponse(status_code=status.HTTP_205_RESET_CONTENT, content={'result': 'successfully deleted!!!'})
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something went wrong!!!')


@image_router.get('/get-employee-image')
def get_employee_image(db: Session = Depends(get_db)):
    try:
        result = jsonable_encoder(db.query(employeeImages).all())
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something went wrong!!!')