from flask import Flask, render_template

class Alunos:
    def __init__(self,nome, idade, turma, data_nascimento, nota_primeiro_s, nota_segundo_s, media_final):
        self.nome = nome #string
        self.idade = idade #int
        self.turma = turma #string
        self.data_nascimento = data_nascimento #date
        self.nota_primeiro_semestre = nota_primeiro_s #float
        self.nota_segundo_semestre = nota_segundo_s #float
        self.media_final = media_final #float

def cadastrar_aluno():
    aluno_1 = Alunos('Diego Leite dos Passos', 22, 'ADS', '26/03/2002', 8.5, 9.0, 8.75)
    aluno_2 = Alunos('Stevenson Lucio Soriano', 21, 'Ciencia da Computação', '15/07/2003', 7.5, 8.0, 7.75)
    aluno_3 = Alunos('Marcela Prucho Claudino', 23, 'Engenharia de Software', '12/12/2001', 9.0, 9.5, 9.25)
    lista_alunos = [aluno_1, aluno_2, aluno_3]
    return render_template()