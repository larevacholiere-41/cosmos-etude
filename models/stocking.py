from datetime import date
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class Batch(BaseModel):
    model_config = ConfigDict(frozen=True)

    reference: str = Field(..., description="Unique reference number of the batch")
    sku: str = Field(..., description="Stock Keeping Unit")
    quantity: int = Field(..., description="Quantity of the batch", ge=0)
    eta: Optional[date] = Field(default=None, description="Estimated time of arrival")


class OrderLine(BaseModel):
    model_config = ConfigDict(frozen=True)

    orderid: str = Field(..., description="Unique identifier of the order")
    sku: str = Field(..., description="Stock Keeping Unit")
    quantity: int = Field(..., description="Quantity of the order line", ge=1)
