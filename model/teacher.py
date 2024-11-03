from database import db

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    matter = db.Column(db.String(150), nullable=False)
    obs = db.Column(db.String(150), nullable=False)

    # Relacionamento: um professor tem várias turmas
    class_rooms = db.relationship('Class_room', back_populates='teacher')
