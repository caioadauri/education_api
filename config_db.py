import mysql.connector
from mysql.connector import errorcode

print('Conectando ao banco de dados...')
try:
    conn = mysql.connector.connect(
        host='127.0.0.1', 
        user='root',
        password='root',
    )
    print('Conectado com sucesso!')
except mysql.connector.Error as err: 
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Usuário ou senha incorretos')
    else: 
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `db_faculdade`;")

cursor.execute("CREATE DATABASE `db_faculdade`;")

cursor.execute("USE `db_faculdade`;")
 
print('DB criado com sucesso!')

print('Criando tabelas...')

TABLES = {}
TABLES['professores'] = ( ''' 
CREATE TABLE `professores` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(100) NOT NULL,
    `idade` INT NOT NULL,
    `materia` VARCHAR(100) NOT NULL,
    `observacao` VARCHAR(100) NOT NULL,
    PRIMARY KEY(`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['usuarios'] = (''' 
CREATE TABLE `usuarios` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(50) NOT NULL,
    `nickname` VARCHAR(30) NOT NULL,
    `senha` VARCHAR(20) NOT NULL,
    PRIMARY KEY(`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['turmas'] = ('''
CREATE TABLE `turmas` (
    `id` INT NOT NULL AUTO_INCREMENT, 
    `descricao` VARCHAR(50) NOT NULL,
    `ativo` BOOLEAN NOT NULL,
    `professor_id` INT NOT NULL,
    PRIMARY KEY(`id`),
    CONSTRAINT fk_professor FOREIGN KEY(`professor_id`) REFERENCES `professores` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES ['alunos'] = (''' 
CREATE TABLE `alunos` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(100) NOT NULL,
    `idade` INT NOT NULL,
    `turma` VARCHAR(50) NOT NULL,
    `data_nascimento` DATE NOT NULL,
    `nota_primeiro_semestre` FLOAT NOT NULL,
    `nota_segundo_semestre` FLOAT NOT NULL,
    `media_final` FLOAT NOT NULL, 
    `turma_id` INT NOT NULL,
    PRIMARY KEY(`id`),
    CONSTRAINT fk_turma FOREIGN KEY (`turma_id`) REFERENCES `turmas`(`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print('Criando tabela {}: '.format(tabela_nome), end='')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err: 
        if err.errno == errorcode.ER_TABLES_EXISTS_ERROR:
            print('Tabela já existe.')
        else: 
            print(err.msg)
    else: 
        print('OK')

usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) values (%s, %s, %s)'
usuarios = [
    ('Pedro Gaspar', 'PGaspar', '@PedroGaspar'),
    ('Joao Silva', 'JSilva', '@JoaoSilva')
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('SELECT * FROM usuarios')
print('------ Usuarios ------')
for usuario in cursor.fetchall():
    print(usuario[1])


professor_sql = 'INSERT INTO professores (nome, idade, materia, observacao) values (%s, %s, %s, %s)'
professores = [
    ('Jucelino Rodrigues Bastos', 33, 'Programação Orientada a Objetos', 'Formado em Ciência da Computação'),
    ('Macia Herculina Costa', 38, 'SQL', 'Pós graudada em Big Data'),
    ('Andre Silva Santos', 27, 'Kotlin', 'Desenvolvedor Mobile' ),
    ('Alexandre Jose Martins', 36,'Lógica de Programação', 'Formado em Banco de Dados')
]
cursor.executemany(professor_sql, professores)

cursor.execute('SELECT * FROM professores')
print('------ Professores ------')
for professor in cursor.fetchall():
    print(professor[1])

turma_sql = 'INSERT INTO turmas (professor_id, descricao, ativo) values (%s, %s, %s)'
turmas = [
    (1,'ADS', True),
    (2,'Ciencia da Computacao', True),
    (3,'Engenharia de Software', True)
]
cursor.executemany(turma_sql, turmas)

cursor.execute('SELECT * FROM turmas')
print('------ Turmas ------')
for turma in cursor.fetchall():
    print(turma[1])

aluno_sql = 'INSERT INTO alunos (nome, idade, turma, data_nascimento, nota_primeiro_semestre, nota_segundo_semestre, media_final, turma_id) values (%s, %s, %s, %s, %s, %s, %s, %s)'
alunos = [
    ('Diego Leite dos Passos', 22, 'ADS', '2002-03-26', 8.5, 9.0, 8.75, 1),
    ('Stevenson Lucio Soriano', 21, 'Ciencia da Computacao', '2003-07-15', 7.5, 8.0, 7.75, 2),
    ('Marcela Prucho Claudino', 23, 'Engenharia de Software', '2001-12-12', 9.0, 9.5, 9.25, 3)
]
cursor.executemany(aluno_sql, alunos)

cursor.execute('SELECT * FROM alunos')
print('------ Alunos ------')
for aluno in cursor.fetchall():
    print(aluno[1])



conn.commit()

cursor.close()
conn.close()
