import fastapi
import methods
from sqlalchemy import *
from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session
from db_models import *
from db_connection import engine, SessionLockal

Base.metadata.create_all(engine)

def get_db():
    db = SessionLockal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

# Регистрация курьера в системе - выполнено

@app.post('/courier')
def post_courier(new_name: str, new_districts: list[str]=Query(None), db: Session = Depends(get_db)):
    new_courier = Courier(
        Name=new_name,
        Districts=new_districts,
        Avg_order_complete_time=0,
        Avg_day_orders=0)
    db.add(new_courier)
    db.commit()
    db.refresh(new_courier)
    return (new_courier)

#Получение информации о всех курьерх в системе -  выполнено


@app.get('/courier')
def get_courier(db: Session = Depends(get_db)):
        data = {}
        couriers = db.query(Courier.Id, Courier.Name).all()
        for courier in couriers:
            data[courier.Id] = courier.Name
        return (data)


#Получение подробной информации о курьере - выполнено

@app.get('/courier/{id}')
def courier_id(id: str, db: Session = Depends(get_db)):
    courier = db.query(Courier).filter(Courier.Id == id).first()
    if(courier != None):
        if(courier.Active_order != None):
            return {"Id": courier.Id,
                    "Имя": courier.Name,
                    "Активный заказ": courier.Active_order,
                    "Cр. время обработки заказа": courier.Avg_order_complete_time,
                    "Ср. количество заказов в день": courier.Avg_day_orders
                    }
        else:
            return {"Id": courier.Id,
                    "Имя": courier.Name,
                    "Активный заказ": None,
                    "Cр. время обработки заказа": courier.Avg_order_complete_time,
                    "Ср. количество заказов в день": courier.Avg_day_orders
                    }
    else:
        return ("Курьер не найден")

#Публикация заказа в системе


@app.post('/order')
def post_order(name: str, district: str, db: Session = Depends(get_db)):
    new_order = Order(
        Name=name,
        District=district,
        Status=1
        )
    couriers_free = db.query(Courier).filter(Courier.Active_order == None).all()
    if(couriers_free != None):
        for courier in couriers_free:
            for i in courier.Districts:
                if(i == new_order.District):
                    new_order.Courier_id = courier.Id
                    courier.Active_order = new_order.Order_id
                    courier.Avg_day_orders += 1
                    db.add(new_order)
                    db.add(courier)
                    db.commit()
                    return (new_order.Courier_id)
    else:
        return("Свободные курьеры не найдены")


#Получение информации о заказе - выполнен


@app.get('/order/{id}')
def get_order_id(id: int, db: Session = Depends(get_db)):
    current_order = db.query(Order).filter(Order.Order_id == id).first()
    if(current_order!= None):
        return (current_order.Order_id, current_order.Status)
    else:
        return ("Заказ не найден")


# Завершить заказ. Должен вернуть ошибку если заказ уже завершен или такого заказа нет


@app.post('/order/{id}')
def post_order_id(id: int, db: Session = Depends(get_db)):
    current_order = db.query(Order).filter(Order.Order_id == id).first()
    if(current_order != None and current_order.status !=2):
        current_order.order_id = 2
        current_order.Courier.Active_order = None
        db.add(current_order)
        db.comit()
        return ("Заказ выполнен")
    else:
        return ("Заказ уже выполнен или вовсе не существует")