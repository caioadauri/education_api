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

   return jsonify({"message": "Professor não encontrado"}), 

@teacher_blueprint.route('/professores', methods=['GET'])
@login_required
def show_teachers():
    teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=teachers)

@teacher_blueprint.route('/professor/new', methods=['GET', 'POST'])
@login_required
def new_teacher():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        matter = request.form.get('matter')
        obs = request.form.get('obs')

        if name:
            teacher = Teacher(name=name, age=age, matter=matter, obs=obs)
            db.session.add(teacher)
            db.session.commit()
            flash("Professor cadastrado com sucesso!", "success")
            return redirect(url_for('teacher.show_teachers'))
        else:
            flash("Erro ao cadastrar professor!", "danger")

    return render_template('new_teacher.html')

@teacher_blueprint.route('/professor/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_teacher(id):
    teacher = Teacher.query.get(id)
    if not teacher:
        flash("Professor não encontrado!", "danger")
        return redirect(url_for('teacher.show_teachers'))

    if request.method == 'POST':
        teacher.name = request.form.get('name')
        teacher.age = request.form.get('age')
        teacher.matter = request.form.get('matter')
        teacher.obs = request.form.get('obs')
        db.session.commit()
        flash("Professor atualizado com sucesso!", "success")
        return redirect(url_for('teacher.show_teachers'))

    return render_template('edit_teacher.html', teacher=teacher)

@teacher_blueprint.route('/professor/deletar/<int:id>', methods=['POST'])
def delete_teacher_html(id):
   
   teacher = Teacher.query.get(id)
   if teacher:
      db.session.delete(teacher)
      db.session.commit()
      flash("Professor deletado com sucesso!", "success")
   else:
      flash("Professor não encontrado!", "danger")
  
   return redirect(url_for('teacher.show_teachers'))