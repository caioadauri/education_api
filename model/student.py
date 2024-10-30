from database import db
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    classroom = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.Date(), nullable=False)
    grade_first_semester = db.Column(db.Float, nullable=False)
    grade_second_semester = db.Column(db.Float, nullable=False)
    average_final = db.Column(db.Float, nullable=False)
    class_id = db.Column(db.Integer, nullable=False)

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