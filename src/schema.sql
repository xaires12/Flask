/* baza danych dla projektu PokeGnomeGO */

CREATE TABLE IF NOT EXISTS user (
	user_id INTEGER
		NOT NULL PRIMARY KEY AUTOINCREMENT,
	login VARCHAR(30)
		NOT NULL UNIQUE,
	password CHAR(64)
		NOT NULL
	);

CREATE TABLE IF NOT EXISTS gnome (
	gnome_id INTEGER
		NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(100)
		NOT NULL UNIQUE,
	longitude FLOAT
		NOT NULL,
	latitude FLOAT
		NOT NULL,
	photo BLOB
		NULL
	);

CREATE TABLE IF NOT EXISTS visit (
	visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER
		NOT NULL,
	gnome_id INTEGER
		NOT NULL,
	photo BLOB
		NULL,
	visit_date DATETIME
		NULL,
	PRIMARY KEY (user_id, gnome_id),
	FOREIGN KEY (user_id) REFERENCES user(user_id),
	FOREIGN KEY (gnome_id) REFERENCES gnome(gnome_id)
	);

CREATE TABLE IF NOT EXISTS user_level (
	level_id INTEGER
		NOT NULL PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(100)
		NOT NULL UNIQUE,
	gnome_count INTEGER
		NOT NULL,
	time_max INTEGER
		NULL
	);

CREATE TABLE IF NOT EXISTS user_comment (
    gnome_id INTEGER
        NOT NULL,
    coment CLOB
        NOT NULL,
    user_id INTEGER
        NOT NULL,
    comment_date DATETIME DEFAULT CURRENT_TIMESTAMP
        NOT NULL,
	FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (visit_id) REFERENCES visit(visit_id)
    );
