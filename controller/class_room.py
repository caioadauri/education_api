from flask import Flask, render_template
from flask_login import current_user, login_required
from flask import Flask, Blueprint, request, jsonify, render_template, flash, redirect, url_for
from model.class_room import Class_room
from database import db

class_blueprint = Blueprint('class', __name__)

@class_blueprint.route('/class', methods=['POST'])
@login_required
def create_class():
  data = request.get_json()
  description = data.get('description')
  teacher_id = data.get('teacher_id')
  active = data.get('active')

  if description:
     class_room = Class_room(description=description, teacher_id=teacher_id, active=active)
     db.session.add(class_room)
     db.session.commit()
     return jsonify({'message':"Turma cadastrada com sucesso!"})
  
  return jsonify({'message': "Erro ao cadastrar Turma!"}), 400 

@class_blueprint.route('/class', methods=['GET'])
@login_required
def get_class():
    class_rooms = Class_room.query.all()
   
    if class_rooms:
       result = [{'id': class_room.id, 'description': class_room.description, 'teacher_id': class_room.teacher_id, 'active': class_room.active} for class_room in class_rooms]
       return jsonify(result)
    
    return jsonify({'message': "Nenhuma Turma cadastrada"}), 400

@class_blueprint.route('/class/<int:id>', methods=['PUT'])
@login_required
def update_class(id):
   data = request.json
   class_room = Class_room.query.get(id)

   if class_room:
      class_room.description = data.get('description')
      class_room.teacher_id = data.get('teacher_id')
      class_room.active = data.get('active')
      db.session.commit()

      return jsonify({'message': "Turma atualizada com sucesso!"})
   
   return jsonify({'message': "Turma não encontrada"}), 404

@class_blueprint.route('/class/<int:id>', methods=['DELETE'])
@login_required
def delete_class(id):
   class_room = Class_room.query.get(id)

   if class_room:
      db.session.delete(class_room)
      db.session.commit()
      return jsonify({"message": "Turma deletda com sucesso"})

   return jsonify({"message": "Turma não encontrada"}), 404