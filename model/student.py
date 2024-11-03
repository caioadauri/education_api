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
    class_id = db.Column(db.Integer, db.ForeignKey('class_room.id'), nullable=False)

    # Relacionamento: cada aluno pertence a uma turma
    class_room = db.relationship('Class_room', back_populates='students')
