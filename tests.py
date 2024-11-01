import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Configurações de conexão usando SQLAlchemy e pymysql
DATABASE_URI = 'mysql+pymysql://root:education@localhost:3306/education-api'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

user_ids = []

def test_create_user():
    new_user_data = {
        "name": "Alice",
        "username": "alice123",
        "password": "securepassword"
    }
    
    session = Session()
    with session.begin():
        result = session.execute(
            text("""INSERT INTO user (name, username, password)
                    VALUES (:name, :username, :password)"""),
            new_user_data
        )
        user_id = result.lastrowid
        user_ids.append(user_id)
    
    session.close()
    
    assert user_id is not None

def test_read_user():
    if user_ids:
        user_id = user_ids[0]
        session = Session()
        with session.begin():
            result = session.execute(text("SELECT * FROM user WHERE id = :id"), {"id": user_id})
            user = result.fetchone()
        
        session.close()
        
        assert user is not None
        assert user.username == "alice123"

def test_update_user():
    if user_ids:
        user_id = user_ids[0]
        updated_data = {
            "name": "Alice Cooper",
            "password": "newpassword123",
            "id": user_id
        }
        
        session = Session()
        with session.begin():
            session.execute(
                text("""UPDATE user SET name = :name, password = :password WHERE id = :id"""),
                updated_data
            )
            result = session.execute(text("SELECT * FROM user WHERE id = :id"), {"id": user_id})
            user = result.fetchone()
        
        session.close()
        
        assert user is not None
        assert user.name == updated_data['name']

def test_delete_user():
    if user_ids:
        user_id = user_ids[0]
        
        session = Session()
        with session.begin():
            session.execute(text("DELETE FROM user WHERE id = :id"), {"id": user_id})
            result = session.execute(text("SELECT * FROM user WHERE id = :id"), {"id": user_id})
            user = result.fetchone()
        
        session.close()
        
        assert user is None
        
teacher_ids = []

def test_create_teacher():
    new_teacher_data = {
        "name": "Caio",
        "age": 30,
        "matter": "Desenvolvimento de APIs",
        "obs": "Desenvolvendo APIs"
    }
    
    session = Session()
    with session.begin():
        result = session.execute(
            text("INSERT INTO teacher (name, age, matter, obs) VALUES (:name, :age, :matter, :obs)"),
            new_teacher_data
        )
        teacher_id = result.lastrowid
        teacher_ids.append(teacher_id)
    
    session.close()
    
    assert teacher_id is not None

def test_get_teachers():
    session = Session()
    with session.begin():
        result = session.execute(text("SELECT * FROM teacher"))
        teachers = result.fetchall()
    
    session.close()
    
    assert isinstance(teachers, list)
    assert len(teachers) > 0

def test_get_teacher():
    if teacher_ids:
        teacher_id = teacher_ids[0]
        session = Session()
        with session.begin():
            result = session.execute(text("SELECT * FROM teacher WHERE id = :id"), {"id": teacher_id})
            teacher = result.fetchone()
        
        session.close()
        
        assert teacher is not None
        assert teacher.id == teacher_id

def test_update_teacher():
    if teacher_ids:
        teacher_id = teacher_ids[0]
        updated_data = {
            "name": "João",
            "age": 28,
            "matter": "SQL",
            "obs": "Criando queries",
            "id": teacher_id
        }
        
        session = Session()
        with session.begin():
            session.execute(
                text("UPDATE teacher SET name = :name, age = :age, matter = :matter, obs = :obs WHERE id = :id"),
                updated_data
            )
            result = session.execute(text("SELECT * FROM teacher WHERE id = :id"), {"id": teacher_id})
            teacher = result.fetchone()
        
        session.close()
        
        assert teacher is not None
        assert teacher.name == updated_data['name']

def test_delete_teacher():
    if teacher_ids:
        teacher_id = teacher_ids[0]
        
        session = Session()
        with session.begin():
            session.execute(text("DELETE FROM teacher WHERE id = :id"), {"id": teacher_id})
            result = session.execute(text("SELECT * FROM teacher WHERE id = :id"), {"id": teacher_id})
            teacher = result.fetchone()
        
        session.close()
        
        assert teacher is None

student_ids = []
def test_create_student():
    new_student_data = {
        "name": "Ana",
        "age": 20,
        "classroom": "101A",
        "date_of_birth": "2003-05-12",
        "grade_first_semester": 85,
        "grade_second_semester": 90,
        "average_final": 87.5,
        "class_id": 1
    }
    
    session = Session()
    with session.begin():
        result = session.execute(
            text("""INSERT INTO student (name, age, classroom, date_of_birth, grade_first_semester,
                                          grade_second_semester, average_final, class_id)
                    VALUES (:name, :age, :classroom, :date_of_birth, :grade_first_semester,
                            :grade_second_semester, :average_final, :class_id)"""),
            new_student_data
        )
        student_id = result.lastrowid
        student_ids.append(student_id)
    
    session.close()
    
    assert student_id is not None

def test_get_students():
    session = Session()
    with session.begin():
        result = session.execute(text("SELECT * FROM student"))
        students = result.fetchall()
    
    session.close()
    
    assert isinstance(students, list)
    assert len(students) > 0

def test_get_student():
    if student_ids:
        student_id = student_ids[0]
        session = Session()
        with session.begin():
            result = session.execute(text("SELECT * FROM student WHERE id = :id"), {"id": student_id})
            student = result.fetchone()
        
        session.close()
        
        assert student is not None
        assert student.id == student_id

def test_update_student():
    if student_ids:
        student_id = student_ids[0]
        updated_data = {
            "name": "Carlos",
            "age": 21,
            "classroom": "102B",
            "date_of_birth": "2002-10-08",
            "grade_first_semester": 92,
            "grade_second_semester": 88,
            "average_final": 90.0,
            "class_id": 2,
            "id": student_id
        }
        
        session = Session()
        with session.begin():
            session.execute(
                text("""UPDATE student SET name = :name, age = :age, classroom = :classroom,
                        date_of_birth = :date_of_birth, grade_first_semester = :grade_first_semester,
                        grade_second_semester = :grade_second_semester, average_final = :average_final,
                        class_id = :class_id WHERE id = :id"""),
                updated_data
            )
            result = session.execute(text("SELECT * FROM student WHERE id = :id"), {"id": student_id})
            student = result.fetchone()
        
        session.close()
        
        assert student is not None
        assert student.name == updated_data['name']

def test_delete_student():
    if student_ids:
        student_id = student_ids[0]
        
        session = Session()
        with session.begin():
            session.execute(text("DELETE FROM student WHERE id = :id"), {"id": student_id})
            result = session.execute(text("SELECT * FROM student WHERE id = :id"), {"id": student_id})
            student = result.fetchone()
        
        session.close()
        
        assert student is None

# BASE_URL = 'http://127.0.0.1:5000'
# teacher = []

# def test_create_teacher():
#   new_teacher_data = {
#     "name": "Caio",
#     "age": 30,
#     "matter": "Desenvolvimento de APIs",
#     "obs": "Desenvolvento APIs"
#   }
#   response = requests.post(f"{BASE_URL}/teacher", json=new_teacher_data)
#   assert response.status_code == 200
#   response_json = response.json()
#   assert "message" in response_json
#   assert "id" in response_json
#   teacher.append(response_json['id'])

# def test_get_teachers():
#   response = requests.get(f"{BASE_URL}/teacher")
#   assert response.status_code == 200
#   response_json = response.json()
#   assert "teachers" in response_json
#   assert "total_teacher" in response_json

# def test_get_teacher():
#   if teacher:
#     teacher_id = teacher[0]
#     response = requests.get(f"{BASE_URL}/teacher/{teacher_id}")
#     assert response.status_code == 200
#     response_json = response.json()
#     assert teacher_id == response_json['id']

# def test_update_teacher():
#   if teacher:
#     teacher_id = teacher[0]
#     payload = {
#       "name": "João",
#       "age": 28,
#       "matter": "SQL",
#       "obs": "Criando querys"
#     }
#     response = requests.put(f"{BASE_URL}/teacher/{teacher_id}", json=payload)
#     assert response.status_code == 200
#     response_json = response.json()
#     assert "message" in response_json

#     response = requests.get(f"{BASE_URL}/teacher/{teacher_id}")
#     assert response.status_code == 200
#     response_json = response.json()
#     assert response_json["name"] == payload["name"]

# def test_delete_teacher():
#   if teacher:
#     teacher_id = teacher[0]
#     response = requests.delete(f"{BASE_URL}/teacher/{teacher_id}")
#     assert response.status_code == 200

#     response = requests.get(f"{BASE_URL}/teacher/{teacher_id}")
#     assert response.status_code == 404