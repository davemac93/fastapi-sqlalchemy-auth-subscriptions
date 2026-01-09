from pydantic import BaseModel
from datatime import datetime
from typing import Optional
from app.models.subscription import PlansOptions, PlansPrices

class UpgradeSubscription(BaseModel):
    option: PlansOptions
    price: PlansPrices

class CancelSubscription(BaseModel):
    option: PlansOptions
    price: PlansPrices

class DowngradeSubscription(BaseModel):
    option: PlansOptions
    price: PlansPrices