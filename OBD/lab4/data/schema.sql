CREATE TABLE "group" (
    code VARCHAR(20) PRIMARY KEY,
    year INT NOT NULL
);

CREATE TABLE student (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(10),
    group_code VARCHAR(20) REFERENCES "group"(code)
);

CREATE TABLE student_card (
    id INT PRIMARY KEY REFERENCES student(id),
    date_of_issue DATE NOT NULL
);

CREATE TABLE course (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    assessment_method VARCHAR(20) NOT NULL
);

CREATE TABLE course_listeners (
    student_id INT REFERENCES student(id),
    course_id INT REFERENCES course(id),
    PRIMARY KEY (student_id, course_id)
);

CREATE TABLE grade (
    student_id INT REFERENCES student(id),
    course_id INT REFERENCES course(id),
    value INT,
    graded_at DATE
);