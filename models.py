from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="user")
    
    
    def __repr__(self):
        return f"<User {self.username}>"
    

class Order(Base):
    
    ORDER_STATUS = (
        ('PENDENTE','pendente'),
        ('A CAMINHO','a caminho'),
        ('ENTREGUE','entregue'),
    )
    
    
    PIZZA_SIZE=(
        ('PEQUENA','pequena'),
        ('MEDIA','media'),
        ('GRANDE','grande'),
        ('FAMILIA','FAMILIA')
    )
    
    
    __tablename__ = "orders"

    id=Column(Integer,primary_key=True)
    quantity=Column(Integer,nullable=False)
    order_status=Column(ChoiceType(choices=ORDER_STATUS),default="PENDENTE")
    pizza_size=Column(ChoiceType(choices=PIZZA_SIZE),default="PEQUENA")
    user_id=Column(Integer,ForeignKey('user.id'))
    user=relationship('User',back_populates='orders')

    def __repr__(self):
        return f"<Order {self.id}>"