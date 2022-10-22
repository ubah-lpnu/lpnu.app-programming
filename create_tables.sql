CREATE TABLE users
(
	id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
	username VARCHAR(45) NOT NULL,
	password VARCHAR(100) NOT NULL,
	email VARCHAR(100) NOT NULL,
	first_name VARCHAR(45) NOT NULL,
	last_name VARCHAR(45) NOT NULL,
	userStatus BOOLEAN NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE notes(
	id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
	owner_id INT NOT NULL,
	title VARCHAR(100) NOT NULL,
	isPublic BOOLEAN NOT NULL,
	text VARCHAR(1000) NOT NULL,
	dateOfEditing DATE NOT NULL,
	PRIMARY KEY(id),
	CONSTRAINT fk_user
	   FOREIGN KEY(owner_id)
	    REFERENCES users(id)
);

CREATE TABLE tags(
	id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
	text VARCHAR(100) NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE tag_note(
	note_id INT NOT NULL,
	tag_id INT NOT NULL,
	PRIMARY KEY(note_id, tag_id),
	CONSTRAINT fk_tag
	   FOREIGN KEY(tag_id)
	    REFERENCES tags(id),
	CONSTRAINT fk_note
	  FOREIGN KEY(note_id)
	    REFERENCES notes(id)
);

CREATE TABLE stats(
	id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
	user_id INT NOT NULL,
	numOfNotes INT NOT NULL,
	numOfEditingNotes INT NOT NULL,
	dateOfCreating DATE NOT NULL,
	PRIMARY KEY(id),
	CONSTRAINT fk_user
	   FOREIGN KEY(user_id)
	    REFERENCES users(id)
);

CREATE TABLE allowed_notes(
	note_id INT NOT NULL,
	user_id INT NOT NULL,
	PRIMARY KEY(note_id, user_id),
	CONSTRAINT fk_user
	   FOREIGN KEY(user_id)
	    REFERENCES users(id),
	CONSTRAINT fk_note
	  FOREIGN KEY(note_id)
	    REFERENCES notes(id)
);