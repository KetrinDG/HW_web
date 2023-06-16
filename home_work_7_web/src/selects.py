from sqlalchemy import func, and_

from src.connect import session
from src.models import Groups, Gradebook, Students, Subjects, Teachers


def res_to_dict(res):
    return [r._asdict() for r in res]


def print_res(res):
    if res:
        title = [key for key, value in res[0].items()]
    length_col = 30
    length = length_col * len(title) + 4
    print("-" * length)
    print_string = "|"
    for _ in title:
        print_string += " {:^" + str(length_col - 2) + "} |"
    print(print_string.format(*title))
    print("-" * length)
    for el in res:
        print(print_string.format(*[str(value) for key, value in el.items()]))
        print("-" * length)
    print_string = "| {:<" + str(length - 4) + "} |"
    print(print_string.format(f"Row: {len(res)}"))
    print("-" * length)


def select_1():
    # Top 5 students with the highest average grade across all subjects
    sql = (
        session.query(
            Students.student_name,
            Groups.group_name,
            func.round(func.avg(Gradebook.grade), 2).label("average_grade"),
        )
        .join(Gradebook)
        .join(Groups)
        .group_by(Students.id, Groups.group_name)
        .limit(5)
    )
    res = sql.all()
    print_res(res_to_dict(res))
    return res_to_dict(res)


def select_2(subject):
    # Students with the highest average grade in a specific subject
    subsql = (
        session.query(
            Gradebook.id_student,
            func.round(func.avg(Gradebook.grade), 2).label("grade"),
        )
        .filter(Gradebook.id_subject == subject)
        .group_by(Gradebook.id_student)
        .subquery()
    )

    subq = session.query(func.max(subsql.c.grade).label("grade")).scalar_subquery()

    sub_from = (
        session.query(subsql.c.id_student, subsql.c.grade)
        .filter(subsql.c.grade == subq)
        .subquery()
    )

    sql = (
        session.query(Students.student_name, Groups.group_name, sub_from.c.grade)
        .join(Groups)
        .join(sub_from, sub_from.c.id_student == Students.id)
        .order_by(Students.student_name)
    )

    res = sql.all()
    print_res(res_to_dict(res))
    return res_to_dict(res)


def select_3(subject):
    # Average grade in groups for a specific subject
    sql = (
        session.query(
            Groups.group_name,
            func.round(func.avg(Gradebook.grade), 2).label("average_grade"),
        )
        .select_from(Gradebook)
        .join(Students)
        .join(Groups)
        .filter(Gradebook.id_subject == subject)
        .group_by(Groups.group_name)
        .order_by(Groups.group_name)
    )
    res = sql.all()
    print_res(res_to_dict(res))
    return res_to_dict(res)


def select_4():
    # Average grade in the entire course
    sql = session.query(func.round(func.avg(Gradebook.grade), 2).label("average_grade"))
    res = sql.scalar()
    print(res)
    return res


def select_5(teacher):
    # Courses taught by a specific teacher
    sql = session.query(Subjects.subject_name).filter(Subjects.id_teacher == teacher)
    res = sql.all()
    print_res(res_to_dict(res))
    return res_to_dict(res)


def select_6(group):
    # List of students in a specific group
    sql = session.query(Students.student_name).filter(Students.id_group == group)
    res = sql.all()
    print_res(res_to_dict(res))
    return res_to_dict(res)


def select_7(group, subject):
    # Grades of students in a specific group for a specific subject
    sql = (
        session.query(
            Gradebook.createdAt.label("grade_date"),
            Students.student_name,
            Gradebook.grade,
        )
        .join(Students)
        .filter(and_((Students.id_group == group), (Gradebook.id_subject == subject)))
        .order_by(Gradebook.createdAt, Students.student_name)
    )
    res = sql.all()
    print_res(res_to_dict(res))
    return res_to_dict(res)


def select_8(teacher):
    # Average grade given by a specific teacher for their subjects
    sql = (
        session.query(
            Subjects.subject_name,
            func.round(func.avg(Gradebook.grade), 2).label("average_grade"),
        )
        .join(Gradebook)
        .filter(Subjects.id_teacher == teacher)
        .group_by(Subjects.subject_name)
    )
    res = sql.all()
    print_res(res_to_dict(res))
    return res_to_dict(res)


def select_9(student):
    # List of courses attended by a student
    sql = (
        session.query(Subjects.subject_name)
        .join(Gradebook)
        .filter(Gradebook.id_student == student)
        .group_by(Subjects.subject_name)
        .order_by(Subjects.subject_name)
    )
    res = sql.all()
    print_res(res_to_dict(res))
    return res_to_dict(res)


def select_10(student, teacher):
    # List of courses taught by a specific teacher to a specific student
    sql = (
        session.query(Subjects.subject_name)
        .join(Gradebook)
        .filter(
            and_((Gradebook.id_student == student), (Subjects.id_teacher == teacher))
        )
        .group_by(Subjects.subject_name)
        .order_by(Subjects.subject_name)
    )
    res = sql.all()
    print_res(res_to_dict(res))
    return res_to_dict(res)


def select_11(student, teacher):
    # Average grade given by a specific teacher to a specific student
    sql = (
        session.query(func.round(func.avg(Gradebook.grade), 2).label("average_grade"))
        .join(Subjects)
        .filter(
            and_((Gradebook.id_student == student), (Subjects.id_teacher == teacher))
        )
    )
    res = sql.scalar()
    print(res)
    return res


def select_12(group, subject):
    # Grades of students in a specific group for a specific subject on the last lesson
    subq = (
        session.query(func.max(Gradebook.createdAt))
        .join(Students)
        .filter(and_((Students.id_group == group), (Gradebook.id_subject == subject)))
        .scalar_subquery()
    )
    sql = (
        session.query(
            Gradebook.createdAt.label("grade_date"),
            Students.student_name,
            Gradebook.grade,
        )
        .join(Students)
        .filter(
            and_(
                (Students.id_group == group),
                (Gradebook.id_subject == subject),
                (Gradebook.createdAt == subq),
            )
        )
    )
    res = sql.all()
    print_res(res_to_dict(res))
    return res_to_dict(res)
