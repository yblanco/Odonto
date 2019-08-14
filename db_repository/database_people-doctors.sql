DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS addresses;
DROP TABLE IF EXISTS districts;
DROP TABLE IF EXISTS provinces;
DROP TABLE IF EXISTS regions;
DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS types;
# Create tables
CREATE TABLE IF NOT EXISTS people
(
    id_persona INT unsigned NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
    last_name VARCHAR(50),
    dni VARCHAR(20),
    address_id INT unsigned,
    status enum('ENABLE','DISABLE') NOT NULL DEFAULT 'ENABLE',
    UNIQUE KEY (dni),
    PRIMARY KEY(id_persona)
) ENGINE=innodb  DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS doctors
(
    id_doctor INT unsigned NOT NULL AUTO_INCREMENT,
    speciality_id INT unsigned,
    tuition_number VARCHAR(100),
    person_id INT unsigned,
    status enum('ENABLE','DISABLE') NOT NULL DEFAULT 'ENABLE',
    address_id INT unsigned,
    UNIQUE KEY (tuition_number),
    UNIQUE KEY (person_id),
    PRIMARY KEY(id_doctor)
) ENGINE=innodb  DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS patients
(
    id_patient INT unsigned NOT NULL AUTO_INCREMENT,
    person_id INT unsigned,
    contact_id INT unsigned,
    status enum('ENABLE','DISABLE') NOT NULL DEFAULT 'ENABLE',
    UNIQUE KEY (person_id),
    PRIMARY KEY(id_patient)
) ENGINE=innodb  DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS provinces
(
    id_province INT unsigned NOT NULL AUTO_INCREMENT,
    id CHARACTER(6),
    name VARCHAR(50),
    region_id CHARACTER(6),
    status enum('ENABLE','DISABLE') NOT NULL DEFAULT 'ENABLE',
    updated_at DATETIME,
    created_at DATETIME,
    PRIMARY KEY(id_province),
    UNIQUE KEY(id)
) ENGINE=innodb  DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS districts
(
    id_disrtict INT unsigned NOT NULL AUTO_INCREMENT,
    id CHARACTER(6),
    name VARCHAR(50),
    region_id CHARACTER(6),
    province_id CHARACTER(6),
    status enum('ENABLE','DISABLE') NOT NULL DEFAULT 'ENABLE',
    created_at DATETIME,
    updated_at DATETIME,
    PRIMARY KEY(id_disrtict),
    UNIQUE KEY(id)
) ENGINE=innodb  DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS regions
(
    id_region INT unsigned NOT NULL AUTO_INCREMENT,
    id CHARACTER(6),
    name VARCHAR(50),
    status enum('ENABLE','DISABLE') NOT NULL DEFAULT 'ENABLE',
    created_at DATETIME,
    updated_at DATETIME,
    PRIMARY KEY(id_region),
    UNIQUE KEY(id)
) ENGINE=innodb  DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS addresses
(
    id_address INT unsigned NOT NULL AUTO_INCREMENT,
    district_id INT unsigned,
    address VARCHAR(255),
    PRIMARY KEY(id_address)
) ENGINE=innodb  DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS types
(
    id_type INT unsigned NOT NULL AUTO_INCREMENT,
    id INT,
    description VARCHAR(100),
    status enum('ENABLE','DISABLE') NOT NULL DEFAULT 'ENABLE',
    type_type enum('1', '2') COMMENT '1: speciality_id | 2: typecontact_id', 
    PRIMARY KEY(id_type)
) ENGINE=innodb  DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS contacts
(
    id_contact INT unsigned NOT NULL AUTO_INCREMENT,
    value VARCHAR(200),
    typecontact_id INT unsigned,
    PRIMARY KEY(id_contact)
) ENGINE=innodb  DEFAULT CHARSET=utf8;


# Create FKs
ALTER TABLE people
    ADD    FOREIGN KEY (address_id)
    REFERENCES addresses(id_address)
;
    
ALTER TABLE doctors
    ADD    FOREIGN KEY (address_id)
    REFERENCES addresses(id_address)
;
    
ALTER TABLE doctors
    ADD    FOREIGN KEY (person_id)
    REFERENCES people(id_persona)
;
    
ALTER TABLE doctors
    ADD    FOREIGN KEY (speciality_id)
    REFERENCES types(id_type)
;
    
ALTER TABLE patients
    ADD    FOREIGN KEY (person_id)
    REFERENCES people(id_persona)
;
    
ALTER TABLE addresses
    ADD    FOREIGN KEY (district_id)
    REFERENCES districts(id_disrtict)
;
    
ALTER TABLE districts
    ADD    FOREIGN KEY (region_id)
    REFERENCES regions(id)
;
    
ALTER TABLE districts
    ADD    FOREIGN KEY (province_id)
    REFERENCES provinces(id)
;
    
ALTER TABLE provinces
    ADD    FOREIGN KEY (region_id)
    REFERENCES regions(id)
;
    
ALTER TABLE contacts
    ADD    FOREIGN KEY (typecontact_id)
    REFERENCES types(id_type)
;
    
ALTER TABLE patients
    ADD   FOREIGN KEY (contact_id)
    REFERENCES contacts(id_contact);    

# Create Indexes