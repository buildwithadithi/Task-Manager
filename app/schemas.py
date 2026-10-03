from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    completed: bool


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

    model_config = {
        "from_attributes": True
    }


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
    
    
class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    
class UserLogin(BaseModel):
    username: str
    password: str
    
    """
    UserCreate
→ registration request

UserLogin
→ login request

UserResponse
→ response to client
    """
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str