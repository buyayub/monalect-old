BEGIN;

CREATE EXTENSION isn;

CREATE TABLE IF NOT EXISTS users(
	id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	username VARCHAR(255) UNIQUE NOT NULL,
	email TEXT UNIQUE NULL,
	membership VARCHAR(5) CHECK (membership in ('none', 'basic', 'pro')) NOT NULL,
	joined DATE NOT NULL DEFAULT CURRENT_DATE,
	password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS courses (
	id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	user_id INT REFERENCES users (id),
	created DATE NOT NULL DEFAULT CURRENT_DATE,
	description TEXT
);	

CREATE TABLE IF NOT EXISTS lessons (
	id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	course INT REFERENCES courses (id),
	lesson_count INT
);

CREATE TABLE IF NOT EXISTS lesson (
	id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	lessons INT REFERENCES lessons(id),
	lesson_order INT
);

CREATE TABLE IF NOT EXISTS question (
	course INT REFERENCES courses(id),
	lesson INT REFERENCES lesson(id),
	question TEXT,
	answer TEXT
);	

CREATE TABLE IF NOT EXISTS textbook
(
	id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	course INT REFERENCES courses (id),
	book ISBN13
	
);

CREATE TABLE IF NOT EXISTS textbook_section
(
	textbook INT REFERENCES textbook (id),
	lesson INT REFERENCES lesson (id),
	start_page INT,
 	end_page INT
);

CREATE TABLE IF NOT EXISTS notebook_section
(
	id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	course INT REFERENCES courses (id),
	text_content TEXT
);



/*
CREATE TABLE IF NOT EXISTS notebook_line
(
	course INT REFERENCES courses (id),
	section INT REFERENCES notebook_section (id),
	text_content TEXT,
	text_order INT,
);*/

COMMIT;
