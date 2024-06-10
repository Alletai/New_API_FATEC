from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import json
from fastapi import FastAPI

app = FastAPI()

class Aluno(BaseModel):
    nome:str
    id:int
    notas: Dict[str,float]

alunos = []

@app.post("/aluno/")
def adicionar_aluno(aluno: Aluno):
    for nota in aluno.notas.values():
        if nota <0 or nota > 10:
            raise HTTPException(status_code=69, detail="Nota invalida, favor inserir uma nota entre 0 e 10")
    aluno.notas ={materia: round(nota,1) for materia, nota in aluno.notas.items()}
    alunos.append(aluno)
    return{"message": "Aluno adicionado"}

@app.get("/alunos/geral")
def get_alunos():
    if not alunos:
        raise HTTPException(status_code=666,detail="Nenhum aluno cadastrado")
    return alunos
    
@app.get("/aluno/{id}")
def get_aluno_by_nota(id:int):
    for aluno in alunos:
        if aluno.id == id:
            return aluno
    raise HTTPException(status_code=420, detail="Aluno não encontrado")

@app.get("/materia/{materia}")
def get_nota_by_materia(materia:str):
    notas_materia = [(aluno.nome,aluno.notas.get(materia)) for aluno in alunos if materia in aluno.notas]
    return notas_materia

json_data = json.dumps([aluno.dict() for aluno in alunos])

with open('data/alunos.json', 'w') as f:
    f.write(json_data)
