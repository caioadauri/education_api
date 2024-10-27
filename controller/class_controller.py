from flask import Flask, render_template

class Turmas:
    def __init__(self,descricao, professor, ativo):
        self.descricao = descricao #string
        self.professor = professor #string 
        self.ativo = ativo #boolean

def criar_turma():
    pass