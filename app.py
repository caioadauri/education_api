from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from config import Config
from database import db
from model.user import User
from model.teacher import Teacher
from model.student import Student
from model.class_room import Class_room
from controller.user import user_blueprint
from controller.teacher import teacher_blueprint
from controller.student import student_blueprint


def create_app():
   app = Flask(__name__)
   app.config.from_object(Config)
   db.init_app(app)

   app.register_blueprint(user_blueprint)
   app.register_blueprint(teacher_blueprint)
   app.register_blueprint(student_blueprint)

   

   with app.app_context():
      db.create_all()
   
   return app

app = create_app()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




@login_manager.user_loader
def load_user(user_id):
   return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
   data = request.json
   username = data.get('username')
   password = data.get('password')

   if username and password:
      
      user = User.query.filter_by(username=username).first()

      if user and user.password == password:
          login_user(user)
          print(current_user.is_authenticated)
          return jsonify({'message': 'Login realizado com sucesso!'})

   return jsonify({'message': 'Credenciais inválidas'}), 400

@app.route('/logout', methods=['POST'])
@login_required
def logout():
   logout_user()
   return jsonify({'message': 'Logout realizado com sucesso!'})

@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                login_user(user)
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('home'))

        flash('Credenciais inválidas', 'danger')
        return redirect(url_for('entrar'))

    return render_template('login.html')

@app.route('/sair', methods=['GET', 'POST'])
@login_required
def sair():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('entrar'))

@app.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('home.html')



if __name__ == "__main__":
  app.run(debug=True)  
# from controller.student_controller import Alunos
# from controller.class_controller import Turmas



# app = Flask(__name__)
# app.secret_key = 'alura'

# app.config['SQLALCHEMY_DATABASE_URI'] = \
#         '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
#             SGBD = 'mysql+mysqlconnector',
#             usuario = 'root',
#             senha = 'root',
#             servidor = 'localhost',
#             database = 'db_faculdade'
# )

# db = SQLAlchemy(app) 

# class Professores(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(100), nullable=False)
#     idade = db.Column(db.Integer, nullable=False)
#     materia = db.Column(db.String(100), nullable=False)
#     observacao = db.Column(db.String(100), nullable=False)

#     def __repr__(self):
#         return '<Name %r>' % self.name

# class Usuarios(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(50), nullable=False)
#     nickname = db.Column(db.String(30), nullable=False)
#     senha = db.Column(db.String(20), nullable=False)

#     def __repr__(self):
#         return '<Name %r>' % self.name
    
# class Turmas(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     descricao = db.Column(db.String(20), nullable=False)
#     professor_id = db.Column(db.Integer, nullable=False)
#     ativo = db.Column(db.Boolean, nullable=False)

#     def __repr__(self):
#         return '<Name %r>' % self.name
    
# class Alunos(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(100), nullable=False)
#     idade = db.Column(db.Integer, nullable=False)
#     turma = db.Column(db.String(50), nullable=False)
#     data_nascimento = db.Column(db.Date, nullable=False)
#     nota_primeiro_semestre = db.Column(db.Float, nullable=False)
#     nota_segundo_semestre = db.Column(db.Float, nullable=False)
#     media_final = db.Column(db.Float, nullable=False)
#     turma_id = db.Column(db.Integer, nullable=False)

#     def __repr__(self):
#         return '<Name %r>' % self.nome


# @app.route('/')
# def index():
#     lista_professores = Professores.query.order_by(Professores.id)
#     lista_alunos = Alunos.query.order_by(Alunos.id)
#     lista_turmas = Turmas.query.order_by(Turmas.id)
#     return render_template('lista.html',
#                            titulo='Cadastro de Professores, Alunos e Turmas',
#                            professores=lista_professores,
#                            alunos=lista_alunos,
#                            turmas=lista_turmas)

# @app.route('/cadastro')
# def cadastro():
#     if 'usuario_autenticado' not in session or session['usuario_autenticado'] == None:
#         return redirect(url_for('login', proxima=url_for('cadastro')))
#     return render_template('novo.html', titulo='Cadastro')



# @app.route('/criar', methods=['POST',])
# def criar():
#     tipo = request.form['tipo']
#     if tipo == 'professor':
#         nome = request.form['nome']
#         idade = request.form['idade']
#         materia = request.form['materia']
#         observacao = request.form['observacao']
        
#         professor = Professores.query.filter_by(nome=nome).first()

#         if professor:
#             flash('Este professor ja esta cadastrado.')
#             return redirect(url_for('index'))
        
#         novo_professor = Professores(nome=nome, idade=idade, materia=materia, observacao=observacao)
#         db.session.add(novo_professor)
#         db.session.commit()

#     elif tipo == 'aluno':
#         nome = request.form['nome']
#         idade = request.form['idade']
#         turma = request.form['turma']
#         data_nascimento = request.form['data_nascimento']
#         nota_primeiro_semestre = request.form['nota_primeiro_s']
#         nota_segundo_semestre = request.form['nota_segundo_s']
#         media_final = request.form['media_final']
        
#         aluno = Alunos.query.filter_by(nome=nome).first()

#         if aluno:
#             flash('Este aluno ja esta cadastrado.')
#             return redirect(url_for('index'))
        
#         novo_aluno = Alunos(nome=nome, idade=idade, turma=turma, data_nascimento=data_nascimento, nota_primeiro_semestre=nota_primeiro_semestre, nota_segundo_semestre=nota_segundo_semestre, media_final=media_final)

#         db.session.add(novo_aluno)
#         db.session.commit()

#     elif tipo == 'turma':
#         descricao = request.form['descricao']
#         professor = request.form['professor']
#         ativo = request.form.get('ativo') == 'on'

#         turma = Turmas.query.filter_by(descricao=descricao).first()

#         if turma:
#             flash('Esta turma esta cadastrada.')
#             return redirect(url_for('index'))
        
#         nova_turma = Turmas(descricao=descricao, professor=professor, ativo=ativo)

#         db.session.add(nova_turma)
#         db.session.commit()

#     return redirect(url_for('index'))

# @app.route('/login')
# def login():
#     proxima = request.args.get('proxima')
#     return render_template('login.html',titulo='Login', proxima=proxima)

# @app.route('/autenticar', methods=['POST',])
# def autenticar():
#     usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
#     if usuario:
#         if request.form['senha'] == usuario.senha:
#             session['usuario_autenticado'] = usuario.nickname
#             flash(usuario.nickname + ' logado com sucesso!')
#             proxima_pagina = request.form['proxima']
#             return redirect(proxima_pagina)
#     else:
#         flash('Senha ou Usuario incorreto.')
#         return redirect(url_for('login'))
    
# @app.route('/logout')
# def logout():
#     session['usuario_autenticado'] = None
#     flash('O logout foi realizado com sucesso!')
#     return redirect(url_for('index'))

# if __name__=='__main__':
#     app.run(debug=True)