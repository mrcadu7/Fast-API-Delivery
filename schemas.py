from typing import Optional
from pydantic import BaseModel


class SignUpModel(BaseModel):
    id:Optional[int]
    username:str
    email:str
    password:str
    is_staff:Optional[bool]
    is_active:Optional[bool]
    
    
    class Config:
        from_attributes=True
        json_schema_extra={
            'example':{
                "id":1,
                "username":"johndoe",
                "email":"johndoe@gmail.com",
                "password":"password",
                "is_staff":False,
                "is_active":True
            }
        }
        

class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_status:Optional[str]="PENDENTE"
    pizza_size:Optional[str]="PEQUENA"
    user_id:Optional[int]
    
    class Config:
        from_attributes=True
        json_schema_extra={
            'example':{
                "quantity":2,
                "order_status":"A CAMINHO",
                "pizza_size":"FAMILIA",
                "user_id":1
            }
        }


class Settings(BaseModel):
    authjwt_secret_key:str="374965cec467ad3a7af863446d63403cfe4746f6d8442ee643395aa5ebe63cde"
    

class LoginModel(BaseModel):
    username:str
    password:str
    
    
class OrderModel(BaseModel):
    quantity:int
    pizza_size:Optional[str]="PEQUENA"
    
    class Config:
        from_attributes=True
        json_schema_extra={
            'example':{
                "quantity":2,
                "pizza_size":"FAMILIA",
            }
        }