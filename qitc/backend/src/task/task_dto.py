from pydantic import BaseModel

class TaskResponse(BaseModel):
    id: int
    name: str
    description: str
    status: str

    class Config:
        orm_mode = True