app.config['SQLALCHEMY_DATABASE_URI'] = \
        '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
            SGBD = 'mysql+mysqlconnector',
            usuario = 'root',
            senha = 'Pe09111998*',
            servidor = 'localhost',
            database = 'db_faculdade'
)