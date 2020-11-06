USE tasklist;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    owner_id BINARY(16) PRIMARY KEY,
    name NVARCHAR(92)
);

DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks (
    uuid BINARY(16) PRIMARY KEY,
    owner_id BINARY(16) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(owner_id) ON DELETE CASCADE,
    description NVARCHAR(1024),
    completed BOOLEAN
);

USE tasklist_test;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    owner_id BINARY(16) PRIMARY KEY,
    name NVARCHAR(92)
);

DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks (
    uuid BINARY(16) PRIMARY KEY,
    owner_id BINARY(16) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(owner_id) ON DELETE CASCADE,
    description NVARCHAR(1024),
    completed BOOLEAN
);
