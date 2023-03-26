DELIMITER //

DROP PROCEDURE IF EXISTS getUserofVideo//

CREATE PROCEDURE getUserofVideo (IN videoId INT)
BEGIN
SELECT * FROM Users WHERE idUser IN (SELECT idUser FROM Videos WHERE idVideo = videoId);
END//

DELIMITER ;