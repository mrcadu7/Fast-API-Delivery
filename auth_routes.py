from fastapi import APIRouter, status, Depends
from database import engine, Session
from schemas import SignUpModel, LoginModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from async_fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

session = Session(bind=engine)


@auth_router.get("/")
async def hello(Authorize: AuthJWT = Depends()):
    
    """
        ## Endpoint para teste de rota
        retorna um "Hello World"
    """
    
    try:
        await Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido")
    return {"message": "Hello World"}


@auth_router.post("/signup", status_code=201)
async def signup(user: SignUpModel):
    
    """
        ## Cria um novo usuário
        Necessita dos seguintes campos:
        ```
            username:int
            email:str
            password:str
            is_staff:bool
            is_active:bool
        ```
    """
    
    db_email=session.query(User).filter(User.email==user.email).first()
    
    if db_email is not None:
        return HTTPException(status_code=400, detail="Email já existe")
    
    db_username=session.query(User).filter(User.username==user.username).first()
    
    if db_username is not None:
        return HTTPException(status_code=400, detail="Usuario já existe")
    
    new_user=User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )
    
    session.add(new_user)
    session.commit()
    
    return new_user


# login route

@auth_router.post("/login", status_code=200)
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    
    """
        ## Loga um usuário
        Necessita dos seguintes campos:
        ```
            username:str
            password:str
        ```
        Retorna um token de acesso
    """
    
    db_user=session.query(User).filter(User.username==user.username).first()
    
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = await Authorize.create_access_token(subject=db_user.username)
        refresh_token = await Authorize.create_refresh_token(subject=db_user.username)
        
        response = {
            "access": access_token,
            "refresh": refresh_token
        }
        
        return jsonable_encoder(response)
    raise HTTPException(status_code=401, detail="Usuario ou senha inválidos")


# refresh route

@auth_router.get("/refresh")
async def refresh(Authorize: AuthJWT = Depends()):
    
    """
        ## Cria um novo token de acesso
        Cria um novo token de acesso com base no token de atualização 
    """
    
    try:
         await Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Por favor, forneça um token de atualização")
    
    current_user = await Authorize.get_jwt_subject()
    
    access_token = await Authorize.create_access_token(subject=current_user)
    
    return jsonable_encoder({"access": access_token})