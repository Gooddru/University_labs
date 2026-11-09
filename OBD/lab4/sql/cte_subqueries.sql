WITH
    -- 1. CTE raw_grades: напишем, чтобы собрать абсолютно всех слушателей курсов и их оценки
    raw_grades AS (SELECT s.id                               AS student_id,
                          s.first_name || ' ' || s.last_name AS student,
                          s.group_code,
                          cl.course_id,
                          g.value                            AS grade_value
                   FROM course_listeners AS cl
                            JOIN grade AS g
                                 ON g.student_id = cl.student_id
                                     AND g.course_id = cl.course_id
                            JOIN student AS s
                                 ON s.id = cl.student_id
                   WHERE g.value IS NOT NULL),

    -- 2. CTE student_stats: считаем количество курсов и средний балл каждого студента по группе
    student_stats AS (SELECT student_id,
                             student,
                             group_code,
                             COUNT(DISTINCT course_id) AS course_count,
                             AVG(grade_value)          AS student_avg
                      FROM raw_grades
                      WHERE group_code IS NOT NULL
                      GROUP BY student_id, student, group_code
                      HAVING COUNT(DISTINCT course_id) >= 2),

    -- 3. CTE group_stats: считаем средний балл по всем курсам студентов в каждой группе
    group_stats AS (SELECT group_code,
                           AVG(grade_value) AS group_avg
                    FROM raw_grades
                    WHERE group_code IS NOT NULL
                    GROUP BY group_code)

-- 4. Итоговый запрос: объединяем результаты CTE, считаем курсы выше среднего и фильтруем результат
SELECT ss.student_id,
       ss.student,
       ss.group_code,
       ss.course_count,
       ROUND(ss.student_avg, 1)                                                          AS student_avg,
       ROUND(gs.group_avg, 1)                                                            AS group_avg,
       (
           -- Коррелированный подзапрос: количество курсов, где оценка студента выше средней по курсу
           SELECT COUNT(DISTINCT rg_outer.course_id)
           FROM raw_grades AS rg_outer
           WHERE rg_outer.student_id = ss.student_id
             AND rg_outer.grade_value > (SELECT AVG(rg_inner.grade_value)
                                         FROM raw_grades AS rg_inner
                                         WHERE rg_inner.course_id = rg_outer.course_id)) AS courses_above_course_avg
FROM student_stats AS ss
         JOIN group_stats AS gs
              ON gs.group_code = ss.group_code
WHERE
  -- Скалярный подзапрос при фильтрации: сравниваем со средней оценкой по всем записям
    ss.student_avg > (SELECT AVG(g_all.value)
                      FROM course_listeners AS cl_all
                               JOIN grade AS g_all
                                    ON g_all.student_id = cl_all.student_id
                                        AND g_all.course_id = cl_all.course_id
                      WHERE g_all.value IS NOT NULL)
  AND ss.student_avg > gs.group_avg
ORDER BY ss.group_code ASC,
         student_avg DESC,
         ss.student_id ASC;