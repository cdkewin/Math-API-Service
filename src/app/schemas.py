from pydantic import BaseModel, Field


class PowerRequest(BaseModel):
    base: float = Field(..., example=2)
    exponent: float = Field(..., example=8)


class SingleInput(BaseModel):
    number: int = Field(..., gt=0, example=5)
