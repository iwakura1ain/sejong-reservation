-- drop tables
DROP TABLE IF EXISTS Reservation;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Room;
DROP TABLE IF EXISTS Token_Blocklist;

-- create tables
CREATE TABLE Room (
	   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	   room_name VARCHAR(40) NOT NULL DEFAULT '',
	   room_address1 VARCHAR(80) NOT NULL DEFAULT '',
	   room_address2 VARCHAR(80) NOT NULL DEFAULT '',
	   is_usable BOOLEAN NOT NULL DEFAULT 0,
	   max_users INT DEFAULT 0,
	   open_time TIME NOT NULL DEFAULT '08:00:00',
	   close_time TIME NOT NULL DEFAULT '20:00:00',
	   location_hash VARCHAR(64),
	   preview_image_name VARCHAR(50) NOT NULL DEFAULT 'no-image.png'
) DEFAULT CHARSET=utf8;

CREATE TABLE User (
	   id VARCHAR(10) NOT NULL PRIMARY KEY,
	   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	   password VARCHAR(128),
	   name VARCHAR(20),
	   dept INT NOT NULL,
	   phone VARCHAR(20),
	   email VARCHAR(50) NOT NULL,
	   type INT NOT NULL,
	   no_show INT DEFAULT 0
) DEFAULT CHARSET=utf8;

CREATE TABLE Reservation (
	   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	   is_valid BOOLEAN NOT NULL DEFAULT 1,
	   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	   reservation_code VARCHAR(8) NOT NULL,
	   reservation_type VARCHAR(12) DEFAULT NULL,
	   reservation_topic VARCHAR(100) DEFAULT '',
	   reservation_date DATE NOT NULL,
	   start_time TIME NOT NULL,
	   end_time TIME NOT NULL,
	   room_id INT NOT NULL,
	   CONSTRAINT reservation_to_room
	   FOREIGN KEY (room_id) REFERENCES Room(id)
	   ON UPDATE CASCADE
	   ON DELETE CASCADE,
	   creator_id VARCHAR(10) NOT NULL,
	   CONSTRAINT reservation_to_user
	   FOREIGN KEY (creator_id) REFERENCES User(id)
	   ON UPDATE CASCADE
	   ON DELETE CASCADE,
	   members JSON NOT NULL DEFAULT '{}'
	   CHECK (JSON_VALID(members)),
	   room_used BOOLEAN NOT NULL DEFAULT 0
) DEFAULT CHARSET=utf8;

CREATE TABLE Token_Blocklist (
       	   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	   jti VARCHAR(36) NOT NULL,
	   type VARCHAR(16) NOT NULL,
	   blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	   user_id VARCHAR(10) NOT NULL,
	   CONSTRAINT blocklist_to_user
	   FOREIGN KEY (user_id) REFERENCES User(id)
	   ON UPDATE CASCADE
	   ON DELETE CASCADE
) DEFAULT CHARSET=utf8;

CREATE USER 'development'@'%' IDENTIFIED BY '1234';

GRANT ALL PRIVILEGES ON *.* TO 'development'@'%' IDENTIFIED BY '1234';

INSERT INTO `Room` (`id`, `room_name`, `room_address1`, `room_address2`) VALUES 
(1, '센835', '대양AI센터', '8층 835호'),
(2, '센836', '대양AI센터', '8층 836호');
