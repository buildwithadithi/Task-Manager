from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    completed: bool
    
class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    
class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None
    
    
    """
TaskCreate
    ↓
Client → Server

TaskUpdate
    ↓
Client → Server

TaskResponse
    ↓
Server → Client
    """