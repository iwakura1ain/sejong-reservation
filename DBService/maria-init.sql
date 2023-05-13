-- drop tables
DROP TABLE IF EXISTS Reservation;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Room;
-- create tables
CREATE TABLE Room (
	   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	   room_name VARCHAR(20) NOT NULL DEFAULT '',
	   room_address1 VARCHAR(20) NOT NULL DEFAULT '',
	   room_address2 VARCHAR(20) NOT NULL DEFAULT '',
	   is_usable BOOLEAN NOT NULL DEFAULT 0,
	   max_users INT DEFAULT 0,
	   preview_image MEDIUMBLOB
) DEFAULT CHARSET=utf8;
CREATE TABLE User (
	   id INT NOT NULL PRIMARY KEY,
	   password VARCHAR(128),
	   name VARCHAR(20),
	   dept INT NOT NULL,
	   phone VARCHAR(20),
	   email VARCHAR(50) DEFAULT '',
	   type INT NOT NULL,
	   no_show INT DEFAULT 0
) DEFAULT CHARSET=utf8;
CREATE TABLE Reservation (
	   id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	   reservation_code VARCHAR(100) DEFAULT '',
	   reservation_topic VARCHAR(100) DEFAULT '',
	   reservation_type INT DEFAULT NULL,
	   reservation_date DATE NOT NULL,
	   start_date TIME NOT NULL,
	   end_date TIME NOT NULL,
	   which_room INT NOT NULL,
	   CONSTRAINT reservation_to_room
	   FOREIGN KEY (which_room) REFERENCES Room(id),
	   creator INT NOT NULL,
	   CONSTRAINT reservation_to_user
	   FOREIGN KEY (creator) REFERENCES User(id),
	   members JSON NOT NULL DEFAULT '[]',
	   room_used BOOLEAN NOT NULL DEFAULT 0
) DEFAULT CHARSET=utf8;
CREATE USER 'development'@'%' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON *.* TO 'development'@'%' IDENTIFIED BY '1234';
-- -- Room sample values
-- INSERT INTO Room (roomName, roomAddress1, roomAddress2, maxUsers) values ('센835','대양AI센터','835호',10);
-- INSERT INTO Room (roomName, roomAddress1, roomAddress2, maxUsers) values ('센836','대양AI센터','836호',10);

-- -- User sample values (isAdmin=0)
-- INSERT INTO User (username, password, email) VALUES ('user1','user1!','user1@sju.ac.kr');
-- INSERT INTO User (username, password, email) VALUES ('user2','user2@','user2@sju.ac.kr');

-- -- User sample values (isAdmin=1)
-- INSERT INTO User (username, password, email, isAdmin) VALUES ('hgildong','hgildong1!','hgildong@sju.ac.kr',true);
-- INSERT INTO User (username, password, email, isAdmin) VALUES ('admin','admin','admin@sejong.ac.kr',true);

-- -- initialize timeslots
-- FOR t IN 1..48 
-- DO
-- 	INSERT Timeslot (timeslot) VALUES (t);
-- END FOR;

-- -- 새로운 예약의 topic, room, date, creator 정보 입력
-- INSERT INTO Reservation (reservationTopic, reservationRoom, reservationDate, reservationType, creator, members)
-- VALUES ('회의실 예약 시스템 API 설계 회의',1,DATE("2023-04-07"),1,(SELECT id FROM User WHERE User.username = "user1"),'["user1","user2"]');
-- -- 새로운 예약의 time 정보 입력
-- FOR t IN 10..12
-- DO
-- 	# 예약 id랑 타임슬롯id 
-- 	INSERT ReservationTime (reservation, timeslot) 
-- 	VALUES ((SELECT id FROM Reservation WHERE Reservation.reservationTopic="회의실 예약 시스템 API 설계 회의"),t); 
-- END FOR;


-- -- 새로운 예약의 topic, room, date, creator 정보 입력
-- INSERT INTO Reservation (reservationTopic, reservationRoom, reservationDate, reservationType, creator, members)
-- VALUES ('컴퓨터공학과 교수 회의',1,DATE("2023-04-08"),1,(SELECT id FROM User WHERE User.username = "admin"),'["admin","user2"]');
-- -- 새로운 예약의 time 정보 입력
-- FOR t IN 17..20
-- DO
-- 	# 예약 id랑 타임슬롯id 
-- 	INSERT ReservationTime (reservation, timeslot) 
-- 	VALUES ((SELECT id FROM Reservation WHERE Reservation.reservationTopic="컴퓨터공학과 교수 회의"),t); 
-- END FOR;
-- -- Timeslot에 room 추가?
-- FOR t IN 17..20
-- DO
-- 	INSERT Timeslot (room)
-- 	VALUES ((SELECT reservationRoom FROM Reservation WHERE Reservation.reservationTopic="컴퓨터공학과 교수 회의")); 
-- END FOR;





