from typing import Optional

from pydantic import BaseModel

class MessageSchema(BaseModel):
    messageDigest: str | None = None
    description: Optional[str] = None