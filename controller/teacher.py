from flask_login import current_user, login_required
from flask import Flask, Blueprint, request, jsonify, render_template
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

# class Professores:
#     def __init__(self,nome,idade,materia,observacao):
#         self.nome=nome #string
#         self.idade=idade #int
#         self.materia=materia #string
#         self.observacao=observacao #string

# def cadastra_professor():
#     professor_1 = Professores('Jucelino Rodrigues Bastos', 33, 'Programação Orientada a Objetos', 'Formado em Ciência da Computação')
#     professor_2 = Professores('Macia Herculina Costa', 38, 'SQL', 'Pós graudada em Big Data')
#     professor_3 = Professores('André Silva Santos', 27, 'Kotlin', 'Desenvolvedor Mobile' )
#     professor_4 = Professores('Alexandre José Martins', 36,'Lógica de Programação', 'Formado em Banco de Dados')
#     lista_professores = [professor_1,professor_2,professor_3,professor_4]
#     return render_template()