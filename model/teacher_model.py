class Teacher:
  def __init__(self, id, name, age, matter, obs) -> None:
    self.id = id
    self.name = name
    self.age = age
    self.matter = matter
    self.obs = obs

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "age": self.age,
      "matter": self.matter,
      "obs": self.obs
      }
    

# class Professores(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(100), nullable=False)
#     idade = db.Column(db.Integer, nullable=False)
#     materia = db.Column(db.String(100), nullable=False)
#     observacao = db.Column(db.String(100), nullable=False)

#     def __repr__(self):
#         return '<Name %r>' % self.name