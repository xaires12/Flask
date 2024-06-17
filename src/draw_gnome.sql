/* lista krasnali NIE znalezionych przez użytkownika o id=1 */
SELECT
    gnome_id
FROM
    gnome
WHERE
    gnome_id NOT IN (
        SELECT
            gnome_id
        FROM
            visit
        WHERE
            visit_date IS NOT NULL
            AND user_id = 1
        )
;
