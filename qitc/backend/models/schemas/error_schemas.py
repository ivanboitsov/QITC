from pydantic import BaseModel

class ErrorSchema(BaseModel):
    description: str