from datetime import datetime, timedelta
import faker
from random import randint
from connect import session
from models import Groups, Gradebook, Students, Subjects, Teachers


def create_data_DB():
    count_group = 3
    count_student = 50
    count_teacher = 5
    count_subject = 8
    count_grade = 20
    count_subject_group = 4
    fake = faker.Faker()

    students = [(fake.name(), randint(1, count_group)) for _ in range(count_student)]
    teachers = [(fake.name(),) for _ in range(count_teacher)]
    subjects = [
        (f"Subject_{i + 1}", randint(1, count_teacher)) for i in range(count_subject)
    ]
    groups = [(f"G_{i + 1}",) for i in range(count_group)]

    grades = []
    d_now = datetime.now()
    group_subject = []
    for i in range(count_group):
        gs = set()
        while len(gs) < count_subject_group:
            gs.add(randint(1, count_subject))
        group_subject.append((i + 1, list(gs)))
    for i in range(len(students)):
        for delta in range(count_grade):
            d = (d_now - timedelta(delta)).strftime("%Y-%m-%d")
            sub = randint(0, len(group_subject[students[i][1] - 1][1]) - 1)
            grades.append(
                (i + 1, group_subject[students[i][1] - 1][1][sub], randint(3, 5), d)
            )

    return {
        "students": students,
        "teachers": teachers,
        "subjects": subjects,
        "groups": groups,
        "grades": grades,
    }


def fill_db():
    data = create_data_DB()
    groups_list = [Groups(group_name=el[0]) for el in data["groups"]]
    students_list = [
        Students(student_name=el[0], group=groups_list[el[1] - 1])
        for el in data["students"]
    ]
    teachers_list = [Teachers(teacher_name=el[0]) for el in data["teachers"]]
    subjects_list = [
        Subjects(subject_name=el[0], teacher=teachers_list[el[1] - 1])
        for el in data["subjects"]
    ]
    grades_lists = [
        Gradebook(
            student=students_list[el[0] - 1],
            subject=subjects_list[el[1] - 1],
            grade=el[2],
            createdAt=el[3],
        )
        for el in data["grades"]
    ]
    session.add_all(subjects_list)
    session.commit()

    tl = set()
    for subject in data["subjects"]:
        tl.add(subject[1] - 1)

    obj_free = []
    for i in range(len(data["teachers"])):
        if i not in tl:
            obj_free.append(Teachers(teacher_name=data["teachers"][i][0]))

    session.add_all(obj_free)
    session.commit()


if __name__ == "__main__":
    fill_db()
