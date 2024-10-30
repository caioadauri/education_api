from flask_login import current_user, login_required
from flask import Blueprint, request, jsonify
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

# class Usuarios:
#     def __init__ (self, nome, nickname, senha):
#         self.nome = nome
#         self.nickname = nickname
#         self.senha = senha
        