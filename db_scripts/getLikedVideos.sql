DELIMITER //

DROP PROCEDURE IF EXISTS getLikedVideos//

CREATE PROCEDURE getLikedVideos (IN usernameIn varchar(255))
BEGIN
SELECT *, usernameIn FROM Videos WHERE idVideo IN (SELECT idVideo FROM Likes WHERE idUser IN (SELECT idUser FROM Users WHERE usernameIn = Users.userName));
END//

DELIMITER ;