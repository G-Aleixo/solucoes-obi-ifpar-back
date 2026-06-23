from pydantic import BaseModel

class ProblemBase(BaseModel):
    name: str
    year: str
    phase: str
    level: str

class ProblemCreate(ProblemBase):
    ...

class ProblemResponse(ProblemBase):
    id: int
    
    class Config:
        from_attributes = True

class SubTaskBase(BaseModel):
    problem_id: int

# This is just a scaffold to group up TestPairs
class SubTaskCreate(SubTaskBase):
    ...

class SubTaskResponse(SubTaskBase):
    id: int
    
    class Config:
        from_attributes = True

class TestPairBase(BaseModel):
    subtask_id: int
    
    installed: bool
    input: str | None
    output: str | None

class TestPairCreate(TestPairBase):
    ...

class TestPairResponse(TestPairBase):
    id: int
    
    class Config:
        from_attributes = True

class AdminBase(BaseModel):
    name: str

class AdminCreate(AdminBase):
    password: str

class AdminResponse(AdminBase):
    id: int