from sqlalchemy import Column, Integer, String, DateTime, PickleType, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, TEXT
from db_connection import Base
from sqlalchemy.orm import relationship, backref


class Order(Base):
    __tablename__ = 'orders'
    Order_id = Column(Integer, primary_key=True)#id заказа
    Name = Column(TEXT)# название заказа
    District = Column(TEXT)#район заказа
    Status = Column(Integer)#статус заказа
    Courier_id = Column(Integer, ForeignKey("couriers.Id"))


class Courier(Base):
    __tablename__ = 'couriers'
    Id = Column(Integer, primary_key=True, autoincrement=True)# id курьера
    Name = Column(TEXT)# имя курьера
    Districts = Column(ARRAY(TEXT))# массив районов
    Avg_order_complete_time = Column(TEXT)# ср. время выполнения заказа
    Avg_day_orders = Column(Integer)# ср. кол-во завершенных заказов в день
    Active_order = relationship("Order",  backref=backref("Courier"), uselist=False)
