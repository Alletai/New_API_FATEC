from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import json

app = FastAPI()

class Aluno(BaseModel):

    nome: str
    id: int
    notas: Dict[str, float]

#Segue Dict das frases e quantidades de vezes que foram ditas
#logo depois que terminei o BaseModel
#
#  frase : foi dita  
# 
# Frase: [
#   {
#      "Seja o que Deus quiser" : 1947,
#      "Eu não sei o que estou fazendo" : 17476,
#      "Deu erro e eu não seri porquê" : 32549,
#      "Nem sei o que aconteceu, mas deu certo" : 73545,
#      "Odeio python" : 27593,
#      "Jesus é maravilhoso" : 7374,
#      "Credo, que negocio feio" : 265,
#      "Meu Deus, me leva" : 35,
#      "Dezani maldito, esse negocio é mt dificil" : 293765456
#   }
# ] 
#

def load_data(file="data.json"):
    try:
        with open(file, "r") as f:
            return [Aluno(**aluno) for aluno in json.load(f)]
    except FileNotFoundError:
        return []

def save_data(alunos, file="data.json"):
    with open(file, "w") as f:
        json.dump([aluno.dict() for aluno in alunos], f)

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
    return alunos or HTTPException(status_code=404, detail="Nenhum aluno cadastrado")

@app.get("/aluno/{id}")
def get_aluno(id: int):
    aluno = next((a for a in alunos if a.id == id), None)
    return aluno or HTTPException(status_code=404, detail="Aluno não encontrado")

@app.get("/materia/{materia}")
def get_nota_by_materia(materia: str):
    notas_materia = [(aluno.nome, aluno.notas.get(materia)) for aluno in alunos if materia in aluno.notas]
    if not notas_materia:
        raise HTTPException(status_code=404, detail="Matéria não encontrada")
    notas_materia.sort(key=lambda x: x[1])
    return [{"nome": nome, "materia": materia, "nota": nota} for nome, nota in notas_materia]
