/* podstawowe dane do bazy danych dla projektu PokeGnomeGO */

INSERT INTO user (login, password)
	VALUES ('test_user', '111a9383ebd1471d3babe11ee355b96e42d1d5900b020d1878840eef633f9c04');
	/* dodanie użytkownika */

INSERT INTO gnome (name, longitude, latitude)
	VALUES ('Automatek', 17.06527777777778, 51.10861111111111);
	/* dodanie krasnala */

INSERT INTO visit (user_id, gnome_id)
	VALUES(1, 1);
	/* użytkownikowi 1 wylosowano krasnala 1 */

UPDATE TABLE visit
SET visit_date = '2024-05-01'
WHERE user_id = 1 AND gnome_id = 1;
/* użytkownik 1 znalazł krasnala 1 */

INSERT INTO user_level (name, gnome_count, time_max)
	VALUES ('Szybki Bill', 10, 14);
	/* 10 krasnali w max 14 dni */

INSERT INTO user_level (name, gnome_count)
	VALUES ('Mistrz', 800);
	/* 800 krasnali bez ograniczeń czasowych */

INSERT INTO user (login, password)
	VALUES ('test_user1', '111a9383edcabcd3dcabe115e355be6e42d1d5900b020d1878840eef633f9c04');
	/* dodanie użytkownika */

INSERT INTO user_comment (visit_id, coment, user_id)
    VALUES(1, 'Komentarz do wizyty', 2);
    /* test_user1 dodaje komentarz do wizyty użytkownika taest_user */
