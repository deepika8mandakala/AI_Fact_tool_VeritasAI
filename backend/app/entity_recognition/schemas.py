from pydantic import BaseModel

class EntityResponse(BaseModel):
    persons: list
    organizations: list
    locations: list
    dates: list
    numbers: list