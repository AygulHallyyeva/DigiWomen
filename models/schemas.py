from pydantic import BaseModel


class baseSchema(BaseModel):
    username: str
    email: str
    phone_number: str
    required: str


class loginSchema(BaseModel):
    email: str
    password: str
    
        
class registerSchema(loginSchema):
    username: str
    retype_password: str