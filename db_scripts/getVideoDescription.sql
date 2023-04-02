DELIMITER //

DROP PROCEDURE IF EXISTS getVideoDescription//

CREATE PROCEDURE getVideoDescription (IN videoId INT)
BEGIN
SELECT videoDescription FROM Videos WHERE idVideo = videoId;
END//

DELIMITER ;