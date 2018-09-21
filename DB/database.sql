CREATE TABLE IF NOT EXISTS status(
  id_status int unsigned NOT NULL AUTO_INCREMENT,
  id int(4) unsigned zerofill NOT NULL,
  name varchar(50) NOT NULL,
  status enum('ENABLE','DISABLE') NOT NULL DEFAULT 'ENABLE',
  PRIMARY KEY(id_status)
) ENGINE=innodb  DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS users (
  id_user int unsigned zerofill NOT NULL AUTO_INCREMENT,
  id varchar(20) NOT NULL,
  name varchar(30) NOT NULL,
  last_name varchar(30) NOT NULL,
  mail varchar(100) NOT NULL,
  username varchar(50) NOT NULL,
  password varchar(80) NOT NULL,
  status_id int unsigned NOT NULL DEFAULT 1,
  image varchar(255) NOT NULL,
  registered_date datetime DEFAULT NULL,
  activated_date datetime DEFAULT NULL,
  last_login datetime DEFAULT NULL,
  PRIMARY KEY (id_user),
  UNIQUE KEY unique_id (id),
  UNIQUE KEY mail_user (mail),
  UNIQUE KEY user_name (username),
  FOREIGN KEY (status_id) REFERENCES status(id_status)
) ENGINE=innodb  DEFAULT CHARSET=utf8;