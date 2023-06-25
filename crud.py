from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from models import *
from sqlalchemy import func, or_
from upload_depends import upload_image
from tokens import create_access_token, decode_token, check_token


def create_crud(req, model, db: Session):
    new_add = model(**req.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add


def read_employee(db: Session):
    result = db.query(
        Employee, 
    ).options(joinedload(Employee.images).load_only('img')).all()
    return result


def delete_employee(id, db: Session):
    db.query(employeeImages).filter(employeeImages.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    new_delete = db.query(Employee).filter(Employee.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    return True


def search_employee(q, db: Session):
    result = db.query(Employee)\
        .filter(
            or_(
                func.lower(Employee.first_name).like(f'%{q}%'),
                func.lower(Employee.last_name).like(f'%{q}%'),
            )
        ).all()
    return result


def create_employee_image(id, file, db: Session):
    upload_image_name = upload_image('profile', file)
    new_add = employeeImages(
        img = upload_image_name,
        employee_id = id
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add


def signUp(req, db: Session):
    if req.password == '' or \
        len(req.password) < 8 or \
            ' ' in req.password or \
                req.password != req.retype_password:
        return -1
    user = db.query(Users).filter(
        or_(
            Users.email == req.email,
            Users.username == req.username
        )
    ).first()
    if user:
        return False
    
    payload = {
        'username': req.username,
        'email': req.email,
        'password': req.password
    }
    token = create_access_token(payload)
    new_add = Users(
        email = req.email,
        password = req.password,
        username = req.username,
        token = token
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return True


def signIn(req, db: Session):
    user = db.query(Users.token).filter(
        and_(
            or_(
                Users.email == req.email,
                Users.username == req.email
            ),
            Users.password == req.password
        )
    ).first()
    if user:
        return user
    
    
def read_users(header_param, db: Session):
    token = check_token(header_param)
    payload = decode_token(token)
    username: str = payload.get('username')
    email: str = payload.get('email')
    password: str = payload.get('password')
    user = db.query(Users)\
        .filter(
            and_(
                Users.username == username, 
                Users.email == email, 
                Users.password == password
            )
        )\
            .first()
    if user:
        return db.query(Users).all()
    else:
        return False
    

def read_user_id(username, password, db: Session):
    user = db.query(Users.id)\
        .filter(and_(Users.username == username, Users.password == password))\
            .first()
    if user:
        return user.id