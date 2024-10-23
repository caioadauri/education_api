from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from controller.professor_controller import Professores  
from controller.usuario_controller import Usuarios
from controller.aluno_controller import Alunos
from controller.turma_controller import Turmas



app = Flask(__name__)
app.secret_key = 'alura'



db = SQLAlchemy(app) 

@app.route('/')
def index():
    lista_professores = Professores.query.order_by(Professores.id)
    lista_alunos = Alunos.query.order_by(Alunos.id)
    lista_turmas = Turmas.query.order_by(Turmas.id)
    return render_template('lista.html',
                           titulo='Cadastro de Professores, Alunos e Turmas',
                           professores=lista_professores,
                           alunos=lista_alunos,
                           turmas=lista_turmas)

@app.route('/cadastro')
def cadastro():
    if 'usuario_autenticado' not in session or session['usuario_autenticado'] == None:
        return redirect(url_for('login', proxima=url_for('cadastro')))
    return render_template('novo.html', titulo='Cadastro')



@app.route('/criar', methods=['POST',])
def criar():
    tipo = request.form['tipo']
    if tipo == 'professor':
        nome = request.form['nome']
        idade = request.form['idade']
        materia = request.form['materia']
        observacao = request.form['observacao']
        
        professor = Professores.query.filter_by(nome=nome).first()

        if professor:
            flash('Este professor ja esta cadastrado.')
            return redirect(url_for('index'))
        
        novo_professor = Professores(nome=nome, idade=idade, materia=materia, observacao=observacao)
        db.session.add(novo_professor)
        db.session.commit()

    elif tipo == 'aluno':
        nome = request.form['nome']
        idade = request.form['idade']
        turma = request.form['turma']
        data_nascimento = request.form['data_nascimento']
        nota_primeiro_semestre = request.form['nota_primeiro_s']
        nota_segundo_semestre = request.form['nota_segundo_s']
        media_final = request.form['media_final']
        
        aluno = Alunos.query.filter_by(nome=nome).first()

        if aluno:
            flash('Este aluno ja esta cadastrado.')
            return redirect(url_for('index'))
        
        novo_aluno = Alunos(nome=nome, idade=idade, turma=turma, data_nascimento=data_nascimento, nota_primeiro_semestre=nota_primeiro_semestre, nota_segundo_semestre=nota_segundo_semestre, media_final=media_final)

        db.session.add(novo_aluno)
        db.session.commit()

    elif tipo == 'turma':
        descricao = request.form['descricao']
        professor = request.form['professor']
        ativo = request.form.get('ativo') == 'on'

        turma = Turmas.query.filter_by(descricao=descricao).first()

        if turma:
            flash('Esta turma esta cadastrada.')
            return redirect(url_for('index'))
        
        nova_turma = Turmas(descricao=descricao, professor=professor, ativo=ativo)

        db.session.add(nova_turma)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html',titulo='Login', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_autenticado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Senha ou Usuario incorreto.')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_autenticado'] = None
    flash('O logout foi realizado com sucesso!')
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)