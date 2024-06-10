from fastapi import FastAPI
from indb import create_alunos

app = FastAPI()

alunos = create_alunos()

@app.get("/")
def get_alunos():
    return {'Alunos': alunos}
