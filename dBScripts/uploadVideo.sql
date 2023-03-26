DELIMITER //

DROP PROCEDURE IF EXISTS uploadVideo //

CREATE PROCEDURE uploadVideo (IN userId INT, IN title varchar(255), IN vDesc varchar(255), IN vPath varchar(255))
BEGIN
INSERT INTO Videos(idUser, videoTitle, videoDescription, videoPath, uploadDate) VALUES (userId, title, vDesc, vPath, (SELECT NOW()));
END//

DELIMITER ;