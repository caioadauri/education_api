from database import db

class Class_room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    # Relacionamento: cada turma tem um professor
    teacher = db.relationship('Teacher', back_populates='class_rooms')
    
    # Relacionamento: uma turma tem vários alunos
    students = db.relationship('Student', back_populates='class_room')
