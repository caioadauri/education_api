class Professores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    materia = db.Column(db.String(100), nullable=False)
    observacao = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name