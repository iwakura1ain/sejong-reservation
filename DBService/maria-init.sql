CREATE TABLE Room (
	   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	   createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	   updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	   roomName VARCHAR(20) NOT NULL DEFAULT '',
	   roomAddress1 VARCHAR(20) NOT NULL DEFAULT '',
	   roomAddress2 VARCHAR(20) NOT NULL DEFAULT '',
	   isUsable BOOLEAN NOT NULL DEFAULT 0,
	   maxUsers INT DEFAULT 0,
	   previewImage MEDIUMBLOB
) DEFAULT CHARSET=utf8;

CREATE TABLE User (
	   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	   createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	   updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

	   username VARCHAR(20),
	   password VARCHAR(128),
	   email VARCHAR(50) DEFAULT '',

	   userType INT NOT NULL DEFAULT 0,
	   isAdmin BOOLEAN NOT NULL DEFAULT 0,
	   noShowCount INT NOT NULL DEFAULT 0,
	   isBanned INT NOT NULL DEFAULT 0	   
) DEFAULT CHARSET=utf8;

CREATE TABLE Timeslot (
	   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	   slot INT NOT NULL,
	   reservedRoomId INT, -- 다른 테이블 room이랑 겹쳐서 안되는듯? 그래서 다른 이름으로 바꿈

	   CONSTRAINT Timeslot_Room
	   FOREIGN KEY (reservedRoomId) REFERENCES Room(id)	   
) DEFAULT CHARSET=utf8;

CREATE TABLE Reservation (
	   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	   createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	   updatedAt TIMESTAMP  DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	   reservationTopic VARCHAR(100) DEFAULT '',
	   reservationDate DATE NOT NULL DEFAULT CURRENT_DATE,
	   reservationType INT DEFAULT NULL,
	   reservationRoom INT,
	   CONSTRAINT Reservation_Room
	   FOREIGN KEY (reservationRoom) REFERENCES Room(id),
	   
	   creator INT,
	   CONSTRAINT Reservation_User
	   FOREIGN KEY (creator) REFERENCES User(id),
	   members JSON NOT NULL DEFAULT '[]',
	   roomUsed BOOLEAN NOT NULL DEFAULT 0	  
) DEFAULT CHARSET=utf8;

CREATE TABLE ReservationTime (
		reservation INT,
	   	CONSTRAINT ReservationTime_Reservation
	   	FOREIGN KEY (reservation) REFERENCES Reservation(id)
	   	ON DELETE CASCADE,
		
	   	timeslot INT,
	   	CONSTRAINT ReservationTime_Timeslot
	   	FOREIGN KEY (timeslot) REFERENCES Timeslot(id)
	   	ON DELETE CASCADE
) DEFAULT CHARSET=utf8;

