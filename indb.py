from alunos import Aluno

list_alunos = []

def create_alunos():
   for i in range(10):
       a =  Aluno(name=f'Aluno {i + 1}', materia=f'Materia {i + 1}', nota = ((i + 1) * 1.5))
       list_alunos.append(a)
       
   return list_alunos