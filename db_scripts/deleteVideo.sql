DELIMITER //

DROP PROCEDURE IF EXISTS deleteVideo //

CREATE PROCEDURE deleteVideo (IN uName varchar(255), IN videoId INT)
BEGIN
DELETE FROM Comments WHERE idVideo = videoId AND idUser IN (SELECT idUser FROM Users WHERE userName = uName);
DELETE FROM Likes WHERE idVideo = videoId AND idUser IN (SELECT idUser FROM Users WHERE userName = uName);
DELETE FROM Videos WHERE idVideo = videoId AND idUser IN (SELECT idUser FROM Users WHERE userName = uName);
END//

DELIMITER ;