## SQLAlchemy with Alembic

We implemented our SQLAlchemy models for tables:

     Table of students;
     Table of groups;
     Table of teachers;
     Table of subjects with the indication of the teacher who reads the subject;
     A table where each student has grades in subjects with an indication of when the grade was received.

We then used `alembic` to create migrations in the database.

We wrote the `seed.py` script and filled the resulting database with random data (~30-50 students, 3 groups, 
5-8 subjects, 3-5 teachers, up to 20 grades for each student from all subjects). We used the `Faker` package 
for filling. SQLAlchemy `session` mechanism was used when filling.

We also made the necessary selections from the obtained database.
For requests, a separate file `my_select.py` was created, where there are 10 functions from `select_1` to `select_10`. 
Execution of the functions returns a result similar to the previous homework. For requests, we use the SQLAlchemy 
`session` mechanism.
