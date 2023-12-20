CREATE TYPE chat_type as ENUM('keyboard_only', 'webcam_only', 'keyboard_webcam');

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  chat_type chat_type NOT NULL,
  password VARCHAR(255) NOT NULL
);