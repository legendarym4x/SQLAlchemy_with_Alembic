from datetime import date, datetime, timedelta
from random import randint, choice
from faker import Faker
from sqlalchemy import select

from conf.db import session
from conf.models import Teacher, Student, Group, Subject, Grade

fake = Faker('uk-UA')


def date_range(start: date, end: date) -> list:
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result


def fill_data():
    groups = ['Group 1', 'Group 2', 'Group 3']
    subjects = ['Biology', 'Chemistry', 'History', 'Mathematics', 'Physics']
    students_count = 50
    teachers_count = 5

    def insert_students():
        group_ids = session.scalars(select(Group.id)).all()
        for _ in range(students_count):
            student = Student(fullname=fake.name(), group_id=choice(group_ids))
            session.add(student)
        session.commit()

    def insert_teachers():
        for _ in range(teachers_count):
            teacher = Teacher(fullname=fake.name())
            session.add(teacher)
        session.commit()

    def insert_groups():
        for group in groups:
            session.add(Group(name=group))
        session.commit()

    def insert_subjects():
        teacher_ids = session.scalars(select(Teacher.id)).all()
        for subject in subjects:
            session.add(Subject(name=subject, teacher_id=choice(teacher_ids)))
        session.commit()

    def insert_grades():
        # the date of the start of the educational process
        start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
        # the date of the end of the educational process
        end_date = datetime.strptime("2023-05-30", "%Y-%m-%d")
        d_range = date_range(start=start_date, end=end_date)
        subject_ids = session.scalars(select(Subject.id)).all()
        student_ids = session.scalars(select(Student.id)).all()

        for d in d_range:  # let's go through each date
            random_id_subject = choice(subject_ids)
            random_ids_student = [choice(student_ids) for _ in range(5)]

            # we go through the list of "lucky" students, add them to the resulting list and generate a rating
            for student_id in random_ids_student:
                grade = Grade(
                    grade=randint(1, 12),
                    date_of=d,
                    student_id=student_id,
                    subjects_id=random_id_subject,
                )
                session.add(grade)
        session.commit()

    insert_teachers()
    insert_subjects()
    insert_groups()
    insert_students()
    insert_grades()


if __name__ == "__main__":
    fill_data()
