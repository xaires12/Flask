/* users and number of found gnomes */

SELECT
    user.user_id,
    user.login,
    count_gnomes.znaleziono
FROM
    user
    INNER JOIN (
        SELECT
            user_id,
            COUNT(gnome_id) AS znaleziono
        FROM
            visit
        GROUP BY
            user_id
        ) count_gnomes
        ON user.user_id = count_gnomes.user_id
WHERE
    1 = 1
