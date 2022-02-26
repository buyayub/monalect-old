BEGIN;

DROP TABLE users CASCADE;
CREATE TABLE IF NOT EXISTS users(
	id VARCHAR(32) PRIMARY KEY UNIQUE NOT NULL,
	username VARCHAR(32) UNIQUE NOT NULL,
	email TEXT UNIQUE,
	membership VARCHAR(5) CHECK (membership in ('none', 'basic', 'pro')) NOT NULL,
	joined DATE NOT NULL DEFAULT CURRENT_DATE,
	passhash TEXT NOT NULL
);

DROP TABLE courses CASCADE;
CREATE TABLE IF NOT EXISTS courses (
	id VARCHAR(32) PRIMARY KEY UNIQUE NOT NULL,
	user_id VARCHAR(32) REFERENCES users (id),
	created DATE NOT NULL DEFAULT CURRENT_DATE,
	title VARCHAR(255),
	description TEXT
);	

DROP TABLE lesson CASCADE;
CREATE TABLE IF NOT EXISTS lesson (
	id VARCHAR(32) PRIMARY KEY UNIQUE NOT NULL,
	course_id VARCHAR(32) REFERENCES courses (id),
	title VARCHAR(255) NOT NULL,
	lesson_order INT
);

DROP TABLE question CASCADE;
CREATE TABLE IF NOT EXISTS question (
	id VARCHAR(32) PRIMARY KEY UNIQUE NOT NULL,
	course_id VARCHAR(32) REFERENCES courses(id),
	lesson VARCHAR(32) REFERENCES lesson(id),
	question TEXT,
	answer TEXT
);	

DROP TABLE textbook CASCADE;
CREATE TABLE IF NOT EXISTS textbook
(
	id VARCHAR(32) PRIMARY KEY UNIQUE NOT NULL,
	course_id VARCHAR(32) REFERENCES courses (id),
	book ISBN13,
	pages INT
);

DROP TABLE textbook_section CASCADE;
CREATE TABLE IF NOT EXISTS textbook_section
(
	textbook VARCHAR(32) REFERENCES textbook (id),
	lesson_id VARCHAR(32) REFERENCES lesson (id),
	start_page INT,
 	end_page INT
);

DROP TABLE notebook_section CASCADE;
CREATE TABLE IF NOT EXISTS notebook_section
(
	id VARCHAR(32) PRIMARY KEY UNIQUE NOT NULL,
	course_id VARCHAR(32) REFERENCES courses (id),
	text_content TEXT
);


/*

CREATE TABLE IF NOT EXISTS notebook_line
(
	course INT REFERENCES courses (id),
	section INT REFERENCES notebook_section (id),
	text_content TEXT,
	text_order INT,
);
 
 */

DROP TABLE sessions;
CREATE TABLE IF NOT EXISTS sessions
(
	session_id VARCHAR(32) UNIQUE NOT NULL PRIMARY KEY,
	user_id VARCHAR(32) REFERENCES users (id) UNIQUE NOT NULL,
	expiry_date DATE
);

DROP TABLE login_attempts;
CREATE TABLE IF NOT EXISTS login_attempts
(
	user_id VARCHAR(32) REFERENCES users (id),
	attempts INT NOT NULL DEFAULT 0
);

DROP TABLE IF EXISTS test CASCADE;
CREATE TABLE IF NOT EXISTS test
(
	id VARCHAR (32) PRIMARY KEY UNIQUE NOT NULL,
	course_id VARCHAR(32) REFERENCES courses(id)
);

DROP TABLE IF EXISTS test_question CASCADE;
CREATE TABLE IF NOT EXISTS test_question
(
	question_id VARCHAR(32) REFERENCES question(id),
	test VARCHAR(32) REFERENCES test(id),
	correct BOOL DEFAULT NULL
);


COMMIT;
