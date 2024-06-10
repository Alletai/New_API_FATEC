from pydantic import BaseModel

class Aluno(BaseModel):
    name: str
    materia: str
    nota: float