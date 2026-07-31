from pydantic import BaseModel


class MobileCreate(BaseModel):
    brand: str
    model: str
    ram: str
    storage: str
    price: float


class MobileResponse(MobileCreate):
    id: int

    model_config = {
        "from_attributes": True
    }