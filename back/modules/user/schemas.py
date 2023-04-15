from pydantic import BaseModel, create_model
from datetime import datetime


class UserBase(BaseModel):
    id: int
    username: int
    name: int
    email: int
    is_active: bool
    is_superuser: bool
    date_joined: datetime
    created_at: datetime
    updated_at: datetime
    groups: list
