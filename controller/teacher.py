from flask_login import current_user, login_required
from flask import Flask, Blueprint, request, jsonify, render_template, flash, redirect, url_for
from model.teacher import Teacher
from database import db

teacher_blueprint = Blueprint('teacher', __name__)

@teacher_blueprint.route('/teacher', methods=['POST'])
@login_required
def create_teacher():
  data = request.get_json()
  name = data.get('name')
  age = data.get('age')
  matter = data.get('matter')
  obs = data.get('obs')

  if name:
     teacher = Teacher(name=name, age=age, matter=matter, obs=obs)
     db.session.add(teacher)
     db.session.commit()
     return jsonify({'message':"Professor cadastrado com sucesso!"})
   
  return jsonify({'message': "Erro ao cadastrar professor!"}), 400

@teacher_blueprint.route('/teacher', methods=['GET'])
@login_required
def get_teachers():
    teachers = Teacher.query.all()
   
    if teachers:
       result = [{'id': teacher.id, 'name': teacher.name, 'age': teacher.age, 'matter': teacher.matter, 'obs': teacher.obs} for teacher in teachers]
       return jsonify(result)
    
    return jsonify({'message': "Nenhum Professor cadastrado"}), 400

@teacher_blueprint.route('/teacher/<int:id>', methods=['GET'])
@login_required
def get_teacher(id):
   teacher = Teacher.query.get(id)
   
   if teacher:
      return jsonify({'name': teacher.name, 'age': teacher.age, 'matter': teacher.matter, 'obs': teacher.obs})
   return jsonify({'message': "Nenhum Professor encontrado"}), 400

@teacher_blueprint.route('/teacher/<int:id>', methods=['PUT'])
@login_required
def update_teacher(id):
   data = request.json
   teacher = Teacher.query.get(id)

   if teacher:
      teacher.name = data.get('name')
      teacher.age = data.get('age')
      teacher.matter = data.get('matter')
      teacher.obs = data.get('obs')
      db.session.commit()

      return jsonify({'message': "Professor atualizado com sucesso!"})
   
   return jsonify({'message': "Professor não encontrato"}), 404

@teacher_blueprint.route('/teacher/<int:id>', methods=['DELETE'])
@login_required
def delete_teacher(id):
   teacher = Teacher.query.get(id)

   if teacher:
      db.session.delete(teacher)
      db.session.commit()
      return jsonify({"message": "Professor deletdao com sucesso"})

   return jsonify({"message": "Professor não encontrado"}), 404

@teacher_blueprint.route('/professor')
@login_required
def index():
    lista_professores = Teacher.query.order_by(Teacher.id).all()
    return render_template('teacher.html',
                           titulo='Lista de Professores',
                           teachers=lista_professores,)

@teacher_blueprint.route('/cadastro')
def cadastro():
    return render_template('novo.html', titulo='Cadastro')

@teacher_blueprint.route('/criar', methods=['POST',])
def criar():
    tipo = request.form['tipo']
    if tipo == 'professor':
        name = request.form['nome']
        age = request.form['idade']
        matter = request.form['materia']
        obs = request.form['observacao']
        
        professor = Teacher.query.filter_by(name=name).first()

        if professor:
            flash('Este professor ja esta cadastrado.')
            return redirect(url_for('index'))
        
        novo_professor = Teacher(name=name, age=age, matter=matter, obs=obs)
        db.session.add(novo_professor)
        db.session.commit()
    
    return redirect(url_for('teacher.index'))