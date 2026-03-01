from pydantic import BaseModel, EmailStr, constr

class User(BaseModel):
    id: int
    name: constr(min_length=1)
    email: EmailStr
    is_active: bool = True

class Escola(BaseModel):
    id: int
    name: constr(min_length=1)
    location: str

class Turma(BaseModel):
    id: int
    escola_id: int
    name: constr(min_length=1)
    year: int

class ContaContabil(BaseModel):
    id: int
    name: constr(min_length=1)
    account_type: str

class Lancamento(BaseModel):
    id: int
    conta_contabil_id: int
    amount: float
    date: str

class Atividade(BaseModel):
    id: int
    turma_id: int
    description: constr(min_length=1)
    date: str

class Feedback(BaseModel):
    id: int
    user_id: int
    activity_id: int
    comment: str
    rating: int
