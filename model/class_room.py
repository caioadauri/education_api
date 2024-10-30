from database import db

class Class_room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), nullable=False)
    teacher_id = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    # def __repr__(self):
    #     return '<Name %r>' % self.name