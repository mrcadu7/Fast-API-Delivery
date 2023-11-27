from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from async_fastapi_jwt_auth import AuthJWT
from models import Order, User
from schemas import OrderModel, OrderStatusModel
from database import Session, engine


order_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

session = Session(bind=engine)


async def authorize(Authorize: AuthJWT):
    try:
        await Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido")

    current_user = await Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    return user


@order_router.get("/")
async def hello(Authorize: AuthJWT = Depends()):
    try:
        await Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return {"message": "Hello World"}


@order_router.post("/order", status_code=201)
async def place_an_order(order:OrderModel,Authorize: AuthJWT = Depends()):
    user = await authorize(Authorize)
    
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


@order_router.get("/orders")
async def list_all_orders(Authorize: AuthJWT = Depends()):
    user = await authorize(Authorize)
    
    if user.is_staff:
        orders = session.query(Order).all()
        
        return jsonable_encoder(orders)
    
    raise HTTPException(status_code=401, detail="Você não tem permissão")


@order_router.get("/orders/{id}")
async def get_order_by_id(id:int,Authorize: AuthJWT = Depends()):
    user = await authorize(Authorize)
    
    if user.is_staff:
        order = session.query(Order).filter(Order.id == id).first()
        
        return jsonable_encoder(order)
    
    raise HTTPException(status_code=401, detail="Não tem permissão")


@order_router.get('/user/orders')
async def get_user_orders(Authorize: AuthJWT = Depends()):
    user = await authorize(Authorize)
    
    return jsonable_encoder(user.orders)


@order_router.get('/user/orders/{id}')
async def get_specific_order(id:int,Authorize: AuthJWT = Depends()):
    user = await authorize(Authorize)
    
    order = user.orders
    
    for o in order:
        if o.id == id:
            return jsonable_encoder(o)
    
    raise HTTPException(status_code=404, detail="Pedido não encontrado")


@order_router.put('/order/update/{id}')
async def update_order(id:int, order:OrderModel, Authorize: AuthJWT = Depends()):
    user = await authorize(Authorize)
    
    order_to_update = session.query(Order).filter(Order.id == id).first()
    
    order_to_update.quantity = order.quantity
    order_to_update.pizza_size = order.pizza_size
    
    session.commit()
    
    response = {
            "id":order_to_update.id,
            "quantity":order_to_update.quantity,
            "pizza_size":order_to_update.pizza_size,
            "order_status":order_to_update.order_status
        }
        
    return jsonable_encoder(response)


@order_router.patch('/order/update/{id}')
async def update_order_status(id:int, order:OrderStatusModel, Authorize: AuthJWT = Depends()):
    user = await authorize(Authorize)
    
    if user.is_staff:
        order_to_update = session.query(Order).filter(Order.id == id).first()
        
        order_to_update.order_status = order.order_status 
        
        session.commit()
        
        response = {
            "id":order_to_update.id,
            "quantity":order_to_update.quantity,
            "pizza_size":order_to_update.pizza_size,
            "order_status":order_to_update.order_status
        }
        
        return jsonable_encoder(response)
    
    raise HTTPException(status_code=401, detail="Não tem permissão")


@order_router.delete('/order/delete/{id}', status_code=204)
async def delete_order(id:int, Authorize: AuthJWT = Depends()):
    user = await authorize(Authorize)
    
    order_to_delete = session.query(Order).filter(Order.id == id).first()
    
    session.delete(order_to_delete)
    
    session.commit()
    
    return order_to_delete