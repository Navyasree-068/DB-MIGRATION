
SET autocommit=0;
USE migration;

/* CREATE TABLE versionTable (version varchar(10) NOT NULL);

 insert into versionTable values("049");
 
*/

DROP TABLE IF EXISTS users051051;

CREATE TABLE IF NOT EXISTS users051 (
  id int(11) NOT NULL auto_increment,
  name varchar(255) NOT NULL,
  address varchar(255) NOT NULL,
  tele varchar(255) NOT NULL,
  PRIMARY KEY  (id)
);

INSERT INTO users051 (name, address, tele)
SELECT * FROM (SELECT 'Rupert', 'Somewhere', '022') AS tmp
WHERE NOT EXISTS (
    SELECT name FROM users051 WHERE name = 'Rupert'
) LIMIT 1;

INSERT INTO users051 (name, address, tele)
SELECT * FROM (SELECT 'John', 'Doe', '023') AS tmp
WHERE NOT EXISTS (
    SELECT name FROM users051 WHERE name = 'John'
) LIMIT 1;

COMMIT;