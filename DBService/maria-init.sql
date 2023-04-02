-- drop tables
DROP TABLE ReservationTime;
DROP TABLE Reservation;
DROP TABLE User;
DROP TABLE Timeslot;
DROP TABLE Room;

-- create tables
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
	   timeslot INT NOT NULL,
	   room INT,

	   CONSTRAINT Timeslot_Room
	   FOREIGN KEY (room) REFERENCES Room(id)	   
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



-- Room sample values
INSERT INTO Room (roomName, roomAddress1, roomAddress2, maxUsers) values ('센835','대양AI센터','835호',10);
INSERT INTO Room (roomName, roomAddress1, roomAddress2, maxUsers) values ('센836','대양AI센터','836호',10);

-- User sample values (isAdmin=0)
INSERT INTO User (username, password, email) VALUES ('user1','user1!','user1@sju.ac.kr');
INSERT INTO User (username, password, email) VALUES ('user2','user2@','user2@sju.ac.kr');

-- User sample values (isAdmin=1)
INSERT INTO User (username, password, email, isAdmin) VALUES ('hgildong','hgildong1!','hgildong@sju.ac.kr',true);
INSERT INTO User (username, password, email, isAdmin) VALUES ('admin','admin','admin@sejong.ac.kr',true);

-- initialize timeslots
INSERT Timeslot(timeslot) VALUES (1);
INSERT Timeslot(timeslot) VALUES (2);
INSERT Timeslot(timeslot) VALUES (3);
INSERT Timeslot(timeslot) VALUES (4);
INSERT Timeslot(timeslot) VALUES (5);
INSERT Timeslot(timeslot) VALUES (6);
INSERT Timeslot(timeslot) VALUES (7);
INSERT Timeslot(timeslot) VALUES (8);
INSERT Timeslot(timeslot) VALUES (9);
INSERT Timeslot(timeslot) VALUES (10);
INSERT Timeslot(timeslot) VALUES (11);
INSERT Timeslot(timeslot) VALUES (12);
-- ...

-- FOR ii IN 1..48 
-- DO
-- 	INSERT INTO Timeslot (timeslot) VALUES (ii);
-- END FOR;

-- SET @i = 1;
-- WHILE (@i <= 48) DO
--   INSERT INTO Timeslot (timeslot) VALUES (@i);
--   SET @i = @i + 1;
-- END WHILE;


-- 새로운 예약의 topic, room, date, creator 정보 입력
INSERT INTO Reservation (reservationTopic, reservationRoom, reservationDate, reservationType, creator, members)
VALUES ('회의실 예약 시스템 API 설계 회의',1,DATE("2023-04-07"),1,(SELECT id FROM User WHERE User.username = "user1"),'["user1","user2"]');
-- 새로운 예약의 time 정보 입력
INSERT INTO ReservationTime (reservation, timeslot) VALUES ((SELECT id FROM Reservation WHERE Reservation.reservationTopic="회의실 예약 시스템 API 설계 회의"),10); # 예약 id랑 타임슬롯id 
INSERT INTO ReservationTime (reservation, timeslot) VALUES (1,11); # 예약 id랑 타임슬롯id 