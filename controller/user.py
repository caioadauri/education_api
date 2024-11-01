from flask_login import current_user, login_required
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from database import db
from model.user import User

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/user', methods=['POST'])
def create_user():
   data = request.json
   name = data.get('name')
   username = data.get('username')
   password = data.get('password')

   if username and password:
      user = User(name=name, username=username, password=password)
      db.session.add(user)
      db.session.commit()
      return jsonify({'message': "Usuário cadastrado com sucesso!"})
   
   return jsonify({'message': "Credenciais inválidas"}), 400

@user_blueprint.route('/user/<int:id_user>', methods=['GET'])
@login_required
def read_user(id_user):
   user = User.query.get(id_user)

   if user:
      return {'name': user.name, 'username': user.username}
   return jsonify({'message': "Usuário não encontrado"}), 404

@user_blueprint.route('/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
   data = request.json
   user = User.query.get(id_user)

   if user and data.get('password'):
      user.name = data.get('name')
      user.password = data.get('password')
      db.session.commit()

      return jsonify({'message': f"Usuário {user.username} atualizado com sucesso!"})
   
   return jsonify({'message: "Usuário não encontrado'}), 404

@user_blueprint.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
   user = User.query.get(id_user)

   if id_user == current_user.id:
      return jsonify({'message': "Deleção não permitida"}), 403
   if user:
      db.session.delete(user)
      db.session.commit()
      return jsonify({'message': "Usuário deletado com sucesso!"})
   
   return jsonify({'message': "Usuário não encontrado"}), 404

@user_blueprint.route('/usuarios', methods=['GET'])
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@user_blueprint.route('/usuario/novo', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            user = User(name=name, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for('user.show_users'))
        else:
            flash("Credenciais inválidas", "danger")

    return render_template('new_user.html')

@user_blueprint.route('/usuario/editar/<int:id_user>', methods=['GET', 'POST'])
def edit_user(id_user):
    user = User.query.get(id_user)
    if not user:
        flash("Usuário não encontrado!", "danger")
        return redirect(url_for('user.show_users'))

    if request.method == 'POST':
        user.name = request.form.get('name')
        user.password = request.form.get('password')
        db.session.commit()
        flash(f"Usuário {user.username} atualizado com sucesso!", "success")
        return redirect(url_for('user.show_users'))

    return render_template('edit_user.html', user=user)

@user_blueprint.route('/usuario/deletar/<int:id_user>', methods=['POST'])
def delete_user_html(id_user):
    user = User.query.get(id_user)

    if id_user == current_user.id:
        flash("Deleção não permitida para o próprio usuário", "warning")
        return redirect(url_for('user.show_users'))

    if user:
        db.session.delete(user)
        db.session.commit()
        flash("Usuário deletado com sucesso!", "success")
    else:
        flash("Usuário não encontrado!", "danger")

    return redirect(url_for('user.show_users'))
        