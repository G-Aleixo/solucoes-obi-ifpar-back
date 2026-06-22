from pydantic import BaseModel

class ProblemBase(BaseModel):
    name: str
    year: str
    phase: str
    level: str

class ProblemCreate(ProblemBase):
    ...

class ProblemResponse(ProblemCreate):
    id: int
    
    class Config:
        from_attributes = True