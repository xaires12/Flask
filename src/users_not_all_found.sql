/* lista użytkowników, którzy nie znaleźli wszystkich krasnali */

SELECT
    user.user_id
FROM
    user
    LEFT JOIN (
        SELECT
            user_id
        FROM
            visit
        WHERE
            visit.visit_date IS NOT NULL
        ) visit_no_date
        ON (user.user_id = visit_no_date.user_id)
WHERE
    1 = 1
GROUP BY
    user.user_id
HAVING
    COUNT(user.user_id) < 
        (
        SELECT
            COUNT(*) AS ile
        FROM
            gnome
        )
;
