import datetime
from fastapi import FastAPI
from pydantic import BaseModel


class get_order(BaseModel):
    name: str
    id: int
    district: str
    status: int


class get_courier(BaseModel):
    id: int
    name: str
    districts: list[str]
    active_order: dict | None
    avg_order_complete_time: str
    avg_day_orders: int

