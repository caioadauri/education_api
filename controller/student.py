from flask import Flask, render_template
from flask_login import current_user, login_required
from flask import Flask, Blueprint, request, jsonify, render_template, flash, redirect, url_for
from model.student import Student
from database import db

student_blueprint = Blueprint('student', __name__)

@student_blueprint.route('/student', methods=['POST'])
@login_required
def create_student():
  data = request.get_json()
  name = data.get('name')
  age = data.get('age')
  classroom = data.get('classroom')
  date_of_birth = data.get('date_of_birth')
  grade_first_semester = data.get('grade_first_semester')
  grade_second_semester = data.get('grade_second_semester')
  average_final = data.get('average_final')
  class_id = data.get('class_id')

  if name:
     student = Student(name=name, age=age, classroom=classroom, date_of_birth=date_of_birth, 
                       grade_first_semester=grade_first_semester, grade_second_semester=grade_second_semester, 
                       average_final=average_final, class_id=class_id)
     db.session.add(student)
     db.session.commit()
     return jsonify({'message':"Aluno cadastrado com sucesso!"})
   
  return jsonify({'message': "Erro ao cadastrar Aluno!"}), 400

@student_blueprint.route('/student', methods=['GET'])
@login_required
def get_students():
    students = Student.query.all()
   
    if students:
       result = [{'id': student.id, 'name': student.name, 'age': student.age, 'classroom': student.classroom, 
                  'date_of_birth': student.date_of_birth, 'grade_first_semester': student.grade_first_semester, 
                  'grade_second_semester': student.grade_second_semester, 'average_final': student.average_final, 
                  'class_id': student.class_id} for student in students]
       return jsonify(result)
    
    return jsonify({'message': "Nenhum Aluno cadastrado"}), 400

@student_blueprint.route('/student/<int:id>', methods=['GET'])
@login_required
def get_teacher(id):
   student = Student.query.get(id)
   
   if student:
      return jsonify({'name': student.name, 'age': student.age, 'classroom': student.classroom, 
                  'date_of_birth': student.date_of_birth, 'grade_first_semester': student.grade_first_semester, 
                  'grade_second_semester': student.grade_second_semester, 'average_final': student.average_final, 
                  'class_id': student.class_id})
   return jsonify({'message': "Nenhum Aluno encontrado"}), 400

@student_blueprint.route('/student/<int:id>', methods=['PUT'])
@login_required
def update_student(id):
   data = request.json
   student = Student.query.get(id)

   if student:
      student.name = data.get('name')
      student.age = data.get('age')
      student.classroom = data.get('classroom')
      student.date_of_birth = data.get('date_of_birth')
      student.grade_first_semester = data.get('grade_first_semester')
      student.grade_second_semester = data.get('grade_second_semester')
      student.average_final = data.get('average_final')
      student.class_id = data.get('class_id')
      db.session.commit()

      return jsonify({'message': "Aluno atualizado com sucesso!"})
   
   return jsonify({'message': "Aluno não encontrato"}), 404

@student_blueprint.route('/student/<int:id>', methods=['DELETE'])
@login_required
def delete_student(id):
   student = Student.query.get(id)

   if student:
      db.session.delete(student)
      db.session.commit()
      return jsonify({"message": "Aluno deletdao com sucesso"})

   return jsonify({"message": "Aluno não encontrado"}), 404

@student_blueprint.route('/aluno')
def index():
    lista_alunos = Student.query.order_by(Student.id).all()
    return render_template('student.html',
                           titulo='Lista de Alunos',
                           students=lista_alunos,)

# class Alunos:
#     def __init__(self,nome, idade, turma, data_nascimento, nota_primeiro_s, nota_segundo_s, media_final):
#         self.nome = nome #string
#         self.idade = idade #int
#         self.turma = turma #string
#         self.data_nascimento = data_nascimento #date
#         self.nota_primeiro_semestre = nota_primeiro_s #float
#         self.nota_segundo_semestre = nota_segundo_s #float
#         self.media_final = media_final #float

# def cadastrar_aluno():
#     aluno_1 = Alunos('Diego Leite dos Passos', 22, 'ADS', '26/03/2002', 8.5, 9.0, 8.75)
#     aluno_2 = Alunos('Stevenson Lucio Soriano', 21, 'Ciencia da Computação', '15/07/2003', 7.5, 8.0, 7.75)
#     aluno_3 = Alunos('Marcela Prucho Claudino', 23, 'Engenharia de Software', '12/12/2001', 9.0, 9.5, 9.25)
#     lista_alunos = [aluno_1, aluno_2, aluno_3]
#     return render_template()