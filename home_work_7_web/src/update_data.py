from sqlalchemy import and_
from src.connect import session
from src.models import Groups, Gradebook, Students, Subjects, Teachers
from src import selects


def prin_list(lists):
    for el in lists:
        print(el)


#  -------------------- TEACHER------------------------------
def insert_teacher(name):
    teacher = Teachers(teacher_name=name)
    session.add(teacher)
    session.commit()


def update_teacher(id, name):
    teacher = session.query(Teachers).get(int(id))
    if not teacher:
        print(f"Teacher with id = {id} does not exist")
        return None
    teacher.teacher_name = name
    session.add(teacher)
    session.commit()


def delete_teacher(id):
    teacher = session.query(Teachers).get(int(id))
    if not teacher:
        print(f"Teacher with id = {id} does not exist")
        return None
    session.delete(teacher)
    session.commit()


def list_teacher():
    teachers = session.query(Teachers).all()
    prin_list(teachers)
    return teachers


#  -------------------- SUBJECT------------------------------


def insert_subject(name, id_teacher):
    teacher = session.query(Teachers).get(int(id_teacher))
    if not teacher:
        print(f"Teacher with id = {id_teacher} does not exist")
        return None
    subject = Subjects(subject_name=name, teacher=teacher)
    session.add(subject)
    session.commit()


def update_subject(id, name, id_teacher):
    subject = session.query(Subjects).get(int(id))
    if not subject:
        print(f"Subject with id = {id} does not exist")
        return None
    if name:
        subject.subject_name = name
    if id_teacher:
        teacher = session.query(Teachers).get(int(id_teacher))
        if not teacher:
            print(f"Teacher with id = {id_teacher} does not exist")
            return None
        subject.teacher = teacher
    session.add(subject)
    session.commit()


def delete_subject(id):
    subject = session.query(Subjects).get(int(id))
    if not subject:
        print(f"Subject with id = {id} does not exist")
        return None
    session.delete(subject)
    session.commit()


def list_subject():
    subjects = session.query(Subjects).all()
    prin_list(subjects)
    return subjects


#  -------------------- GROUP------------------------------
def insert_group(name):
    group = Groups(group_name=name)
    session.add(group)
    session.commit()


def update_group(id, name):
    group = session.query(Groups).get(int(id))
    if not group:
        print(f"Group with id = {id} does not exist")
        return None
    group.group_name = name
    session.add(group)
    session.commit()


def delete_group(id):
    group = session.query(Groups).get(int(id))
    if not group:
        print(f"Group with id = {id} does not exist")
        return None
    session.delete(group)
    session.commit()


def list_group():
    group = session.query(Groups).all()
    prin_list(group)
    return group


#  -------------------- STUDENT------------------------------


def insert_student(name, id_group):
    group = session.query(Groups).get(int(id_group))
    if not group:
        print(f"Group with id = {id_group} does not exist")
        return None
    student = Students(student_name=name, group=group)
    session.add(student)
    session.commit()


def update_student(id, name, id_group):
    student = session.query(Students).get(int(id))
    if not student:
        print(f"Student with id = {id} does not exist")
        return None
    if name:
        student.student_name = name
    if id_group:
        group = session.query(Groups).get(int(id_group))
        if not group:
            print(f"Group with id = {id_group} does not exist")
            return None
        student.group = group
    session.add(student)
    session.commit()


def delete_student(id):
    student = session.query(Students).get(int(id))
    if not student:
        print(f"Student with id = {id} does not exist")
        return None
    session.delete(student)
    session.commit()


def list_student():
    student = session.query(Students).all()
    prin_list(student)
    return student


#  -------------------- GRADEBOOK------------------------------


def insert_grade(id_student, id_subject, grade, date):
    student = session.query(Students).get(int(id_student))
    if not student:
        print(f"Student with id = {id_student} does not exist")
        return None
    subject = session.query(Subjects).get(int(id_subject))
    if not subject:
        print(f"Subject with id = {id_subject} does not exist")
        return None
    grade = Gradebook(grade=grade, createdAt=date, student=student, subject=subject)
    session.add(grade)
    session.commit()


def update_grade(id_student, id_subject, date, new_grade):
    grade = (
        session.query(Gradebook)
        .filter(
            and_(
                Gradebook.id_student == id_student,
                Gradebook.id_subject == id_subject,
                Gradebook.createdAt == date,
            )
        )
        .one()
    )
    if not grade:
        print(f"Record does not exist")
        return None
    if new_grade:
        grade.grade = new_grade

    session.add(grade)
    session.commit()


def delete_grade(id_student, id_subject, date):
    grade = (
        session.query(Gradebook)
        .filter(
            and_(
                Gradebook.id_student == id_student,
                Gradebook.id_subject == id_subject,
                Gradebook.createdAt == date,
            )
        )
        .one()
    )
    if not grade:
        print(f"Record does not exist")
        return None
    session.delete(grade)
    session.commit()


def list_grade():
    student = session.query(Gradebook).all()
    prin_list(student)
    return student
