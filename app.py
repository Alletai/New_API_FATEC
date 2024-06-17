from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import json

app = FastAPI()

class Aluno(BaseModel):
    nome: str
    id: int
    notas: Dict[str, float]

def load_data(file="data.json"):
    try:
        with open(file, "r") as f:
            return [Aluno(**aluno) for aluno in json.load(f)]
    except:
        return []

def save_data(alunos, file="data.json"):
    with open(file, "w") as f:
        json.dump([dict(aluno) for aluno in alunos], f)

alunos = load_data()

@app.post("/aluno/")
def adicionar_aluno(aluno: Aluno):
    if any(a.id == aluno.id for a in alunos):
        raise HTTPException(status_code=400, detail="Id já existe")

    if any(nota < 0 or nota > 10 for nota in aluno.notas.values()):
        raise HTTPException(status_code=400, detail="Nota inválida, favor inserir uma nota entre 0 e 10")   

    aluno.notas = {materia: round(nota, 1) for materia, nota in aluno.notas.items()}
    alunos.append(aluno)
    save_data(alunos)
    return {"message": " Deu certo"}

@app.get("/alunos/")
def get_alunos():
    if alunos:
        return alunos
    else:
        raise HTTPException(status_code=404, detail="Nenhum aluno cadastrado")

@app.get("/aluno/{id}")
def get_aluno(id: int):
    for aluno in alunos:
        if aluno.id == id:
            return aluno
    raise HTTPException(status_code=404, detail="Aluno não encontrado")

@app.get("/materia/{materia}")
def get_nota_by_materia(materia: str):
    notas_materia = [(aluno.nome, aluno.notas.get(materia)) for aluno in alunos if materia in aluno.notas]
    if notas_materia:
        notas_materia.sort(key=lambda x: x[1])
        alunos_abaixo = [aluno for aluno in notas_materia if aluno[1] < 6.0]
        return {"alunos_com_desempenho_baixo": alunos_abaixo,
                "todos_alunos": [{"nome": nome, "materia": materia, "nota": nota} for nome, nota in notas_materia]}
    else:
        raise HTTPException(status_code=404, detail="Matéria não encontrada")

@app.delete("/aluno/")
def remover_alunos_sem_notas():
    global alunos
    alunos_com_notas = [aluno for aluno in alunos if any(nota != 0 for nota in aluno.notas.values())]
    removidos = len(alunos) - len(alunos_com_notas)
    alunos = alunos_com_notas
    save_data(alunos)
    return {"message": f"foram removidos {removidos} alunos"}
