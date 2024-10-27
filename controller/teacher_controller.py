from flask import Flask, render_template

class Professores:
    def __init__(self,nome,idade,materia,observacao):
        self.nome=nome #string
        self.idade=idade #int
        self.materia=materia #string
        self.observacao=observacao #string

def cadastra_professor():
    professor_1 = Professores('Jucelino Rodrigues Bastos', 33, 'Programação Orientada a Objetos', 'Formado em Ciência da Computação')
    professor_2 = Professores('Macia Herculina Costa', 38, 'SQL', 'Pós graudada em Big Data')
    professor_3 = Professores('André Silva Santos', 27, 'Kotlin', 'Desenvolvedor Mobile' )
    professor_4 = Professores('Alexandre José Martins', 36,'Lógica de Programação', 'Formado em Banco de Dados')
    lista_professores = [professor_1,professor_2,professor_3,professor_4]
    return render_template()