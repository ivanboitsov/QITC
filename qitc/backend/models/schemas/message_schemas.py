from typing import Optional

from pydantic import BaseModel

class MessageSchema(BaseModel):
    messageDigest: str
    description: Optional[str] = None