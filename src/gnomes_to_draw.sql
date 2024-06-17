/* lista krasnoludków do wylosowania dla użytkownika */

SELECT
    gnome.gnome_id
FROM
    gnome
    LEFT JOIN (
        SELECT
            gnome_id
        FROM
            visit
        WHERE
            1 = 1
            AND visit_date IS NOT NULL
            AND user_id = 2  -- dla użytkownika
        ) visit_no_date
        ON (gnome.gnome_id = visit_no_date.gnome_id)
WHERE
    1 = 1
    AND visit_no_date.gnome_id IS NULL
