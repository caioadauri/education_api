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
      return jsonify({"message": "Aluno deletdo com sucesso"})

   return jsonify({"message": "Aluno não encontrado"}), 404

@student_blueprint.route('/alunos', methods=['GET'])
@login_required
def show_students():
   students = Student.query.all()
   return render_template('students.html', students=students)

@student_blueprint.route('/aluno/novo', methods=['GET', 'POST'])
@login_required
def new_student():
   if request.method == 'POST':
      name = request.form.get('name')
      age = request.form.get('age')
      classroom = request.form.get('classroom')
      date_of_birth = request.form.get('date_of_birth')
      grade_first_semester = request.form.get('grade_first_semester')
      grade_second_semester = request.form.get('grade_second_semester')
      average_final = request.form.get('average_final')
      class_id = request.form.get('class_id')

      if name:
         student = Student(name=name, age=age, classroom=classroom, date_of_birth=date_of_birth,
                           grade_first_semester=grade_first_semester, grade_second_semester=grade_second_semester,
                           average_final=average_final, class_id=class_id)
         db.session.add(student)
         db.session.commit()
         flash("Aluno cadastrado com sucesso!", "success")
         return redirect(url_for('student.show_students'))
      else:
         flash("Erro ao cadastrar Aluno!", "danger")

   return render_template('new_student.html')


@student_blueprint.route('/aluno/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
   student = Student.query.get(id)
   if not student:
      flash("Aluno não encontrado!", "danger")
      return redirect(url_for('student.show_students'))
   
   if request.method == 'POST':
      student.name = request.form.get('name')
      student.age = request.form.get('age')
      student.classroom = request.form.get('classroom')
      student.date_of_birth = request.form.get('date_of_birth')
      student.grade_first_semester = request.form.get('grade_first_semester')
      student.grade_second_semester = request.form.get('grade_second_semester')
      student.average_final = request.form.get('average_final')
      student.class_id = request.form.get('class_id')
      db.session.commit()
      flash("Aluno atualizado com sucesso!", "success")

      return redirect(url_for('student.show_students'))
   
   return render_template('edit_student.html', student=student)

@student_blueprint.route('/aluno/deletar/<int:id>', methods=['POST'])
@login_required
def delete_student_html(id):
   student = Student.query.get(id)
   if student:
      db.session.delete(student)
      db.session.commit()
      flash("Aluno deletado com sucesso!", "success")
   else:
      flash("Aluno não encontrado!", "danger")
  
   return redirect(url_for('student.show_students'))