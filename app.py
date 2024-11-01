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
from controller.class_room import class_blueprint


def create_app():
   app = Flask(__name__)
   app.config.from_object(Config)
   db.init_app(app)

   app.register_blueprint(user_blueprint)
   app.register_blueprint(teacher_blueprint)
   app.register_blueprint(student_blueprint)
   app.register_blueprint(class_blueprint)

   

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