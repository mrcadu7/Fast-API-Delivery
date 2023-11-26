from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from async_fastapi_jwt_auth import AuthJWT
from models import Order, User
from schemas import OrderModel
from database import Session, engine

order_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

session = Session(bind=engine)


@order_router.get("/")
async def hello(Authorize: AuthJWT = Depends()):
    try:
        await Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return {"message": "Hello World"}


@order_router.post("/order", status_code=201)
async def place_an_order(order:OrderModel,Authorize: AuthJWT = Depends()):
    try:
        await Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    current_user = await Authorize.get_jwt_subject()
    
    user = session.query(User).filter(User.username == current_user).first()
    
    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity,
    )
    
    new_order.user = user
    
    session.add(new_order)

    session.commit()
    
    response={
        "pizza_size":new_order.pizza_size,
        "quantity":new_order.quantity,
        "id":new_order.id,
        "order_status":new_order.order_status
    }

    return jsonable_encoder(response)