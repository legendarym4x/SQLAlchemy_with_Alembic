from sqlalchemy import func, desc

from conf.models import Student, Teacher, Subject, Grade, Group
from conf.db import session


def select_one():
    """
    -- Find the 5 students with the highest average grade across all subjects
    select
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) as average_grade
        from students s
        join grades g on s.id = g.student_id
        group by s.id
        order by average_grade desc
        limit 5;
    """
    result = (
        session.query(
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label('average_grade'))
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc('average_grade'))
        .limit(5)
        .all()
    )
    return result


def select_two():
    """
    -- Find the student with the highest average grade in a particular subject
    select
        s.id,
        s.fullname,
        round(avg(g.grade), 2) as average_grade
    from students s
    join grades g on s.id = g.student_id
    where g.subject_id = 1  -- replace with a specific 'id' of the subject
    group by s.id
    order by average_grade desc
    limit 1;
    """
    result = (
        session.query(
            Student.id,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label('average_grade')
        )
        .join(Grade, Student.id == Grade.student_id)
        .filter(Grade.subjects_id == 1)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(1)
        .all()
    )
    return result


def select_three():
    """
    -- Find the average score in groups for a certain subject
    select
        g.subject_id,
        s.group_id,
        round(avg(g.grade), 2) as average_grade
    from grades g
    join students s on g.student_id = s.id
    where g.subject_id = 5  -- replace with a specific 'id' of the subject
    group by g.subject_id, s.group_id
    order by g.subject_id, s.group_id;
    """
    result = (
        session.query(
            Grade.subjects_id,
            Student.group_id,
            func.round(func.avg(Grade.grade), 2).label('average_grade')
        )
        .join(Student, Grade.student_id == Student.id)
        .filter(Grade.subjects_id == 2)
        .group_by(Grade.subjects_id, Student.group_id)
        .order_by(Grade.subjects_id, Student.group_id)
        .all()
    )
    return result


def select_four():
    """
    -- Find the average grade on a stream (across the entire grade table)
    select
        round(avg(grade), 2) as average_grade
    from grades;
    """
    result = (
        session.query(func.round(func.avg(Grade.grade), 2).label('average_grade'))
        .scalar()
    )
    return result


def select_five():
    """
    -- Find what courses a particular teacher teaches
    select
        t.fullname as teacher_name,
        s.name as course_name
    from teachers t
    join subjects s on t.id = s.teacher_id
    where t.id = 1; -- replace with a specific teacher ID
    """
    result = (
        session.query(
            Teacher.fullname.label('teacher_name'),
            Subject.name.label('course_name')
        )
        .join(Subject, Teacher.id == Subject.teacher_id)
        .filter(Teacher.id == 5)
        .all()
    )
    return result


def select_six():
    """
    -- Find a list of students in a specific group
    select
        id as student_id,
        fullname as student_name
    from students s
    where group_id = 1; -- replace with a specific group ID
    """
    result = (
        session.query(
            Student.id.label('student_id'),
            Student.fullname.label('student_name')
        )
        .filter(Student.group_id == 1)
        .all()
    )
    return result


def select_seven():
    """
    -- Find the grades of students in a separate group for a specific subject
    select
        s.group_id,
        s.fullname as student_name,
        g.grade
    from students s
    join grades g on s.id = g.student_id
    where
        s.group_id = 1 -- replace with a specific group ID
        and g.subject_id = 2 -- replace with a specific subject ID
    """
    result = (
        session.query(
            Student.group_id,
            Student.fullname.label('student_name'),
            Grade.grade
        )
        .join(Grade, Student.id == Grade.student_id)
        .filter(Student.group_id == 2, Grade.subjects_id == 2)
        .all()
    )
    return result


def select_eight():
    """
    -- Find the grades of students in a separate group for a specific subject
    select
        t.fullname as teacher_name,
        round(avg(g.grade), 2) as average_grade
    from teachers t
    join subjects s on t.id = s.teacher_id
    join grades g on s.id = g.subject_id
    group by t.id, t.fullname;
    """
    result = (
        session.query(
            Teacher.fullname.label('teacher_name'),
            func.round(func.avg(Grade.grade), 2).label('average_grade')
        )
        .join(Subject, Teacher.id == Subject.teacher_id)
        .join(Grade, Subject.id == Grade.subjects_id)
        .group_by(Teacher.id, Teacher.fullname)
        .all()
    )
    return result


def select_nine():
    """
    -- Find a list of courses a student is taking
    select
        s.fullname as student_name,
        sub.name as course_name
    from students s
    join grades g on s.id = g.student_id
    join subjects sub on g.subject_id = sub.id
    where s.id = 1 -- Replace with a specific student 'id'
    group by s.id, sub.name;
    """
    result = (
        session.query(
            Student.fullname.label('student_name'),
            Subject.name.label('course_name')
        )
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subjects_id == Subject.id)
        .filter(Student.id == 3)
        .group_by(Student.id, Subject.name)
        .all()
    )
    return result


def select_ten():
    """
    -- Find a list of courses taught to a specific student by a specific teacher
    select
        s.fullname as student_name,
        sub.name as subject,
        t.fullname as teacher_name
    from students s
    join grades g on s.id = g.student_id
    join subjects sub on g.subject_id = sub.id
    join teachers t on sub.teacher_id = t.id
    where
        s.id = 2 -- replace with a specific student 'id'
        and t.id = 3 -- replace with a specific teacher 'id'
    """
    result = (
        session.query(
            Student.fullname.label('student_name'),
            Subject.name.label('subject'),
            Teacher.fullname.label('teacher_name')
        )
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subjects_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Student.id == 2, Teacher.id == 3)
        .all()
    )
    return result


if __name__ == '__main__':
    # print(select_one())
    # print(select_two())
    # print(select_three())
    # print(select_four())
    # print(select_six())
    # print(select_seven())
    # print(select_eight())
    # print(select_nine())
    print(select_ten())
