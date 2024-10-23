class Turmas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(20), nullable=False)
    professor_id = db.Column(db.Integer, nullable=False)
    ativo = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name