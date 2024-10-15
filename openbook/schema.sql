DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS note;
DROP TABLE IF EXISTS movie;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS list;
DROP TABLE IF EXISTS list_item;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

/* parent comment? */
/* parent post  */

CREATE TABLE comment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  body TEXT NOT NULL,
  FOREIGN KEY (post_id) REFERENCES post (id),
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE note (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE movie (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  director TEXT,
  casts TEXT, 
  year INTEGER, 
  genres TEXT,
  vibes TEXT,
  tags TEXT,
  setting TEXT, 
  country TEXT, 
  image TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE book (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  author TEXT,
  year INTEGER, 
  genres TEXT,
  series TEXT,
  vibes TEXT,
  tags TEXT,
  setting TEXT, 
  country TEXT, 
  image TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE game (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  developer TEXT,
  year INTEGER, 
  genres TEXT,
  series TEXT,
  vibes TEXT,
  tags TEXT,
  setting TEXT, 
  country TEXT, 
  platforms TEXT,
  image TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE list (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  

  title TEXT NOT NULL,
  item TEXT NOT NULL, -- you can't have "lists or arrays" in sqlite, you can have an infinite amount of entries though, have this as a seperate table
  price REAL,
  isComplete BOOLEAN,




  developer TEXT,
  year INTEGER, 
  genres TEXT,
  series TEXT,
  vibes TEXT,
  tags TEXT,
  setting TEXT, 
  country TEXT, 
  platforms TEXT,
  image TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);


CREATE TABLE list_item (





);












