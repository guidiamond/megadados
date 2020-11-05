DROP DATABASE IF EXISTS tasklist;
CREATE DATABASE tasklist;

DROP DATABASE IF EXISTS tasklist_test;
CREATE DATABASE tasklist_test;

DROP USER IF EXISTS tasklist_admin@'%';
CREATE USER tasklist_admin@'%' IDENTIFIED BY "$DB_TASKLIST_ADMIN_PW";
GRANT ALL ON tasklist.* TO tasklist_admin@'%';
GRANT ALL ON tasklist_test.* TO tasklist_admin@'%';

DROP USER IF EXISTS tasklist_app@'%';
CREATE USER tasklist_app@'%' IDENTIFIED BY "$DB_TASKLIST_APP_PW";
GRANT SELECT, INSERT, UPDATE, DELETE ON tasklist.* TO tasklist_app@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON tasklist_test.* TO tasklist_app@'%';

COMMIT
