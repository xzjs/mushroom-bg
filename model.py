from pydantic import BaseModel


class Size(BaseModel):
    min: int
    max: int


class Signal(BaseModel):
    action: str
