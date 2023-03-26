DELIMITER //

DROP PROCEDURE IF EXISTS deleteVideo //

CREATE PROCEDURE deleteVideo (IN videoId INT)
BEGIN
DELETE FROM Comments WHERE idVideo = videoId;
DELETE FROM Likes WHERE idVideo = videoId;
DELETE FROM Videos WHERE idVideo = videoId;
END//

DELIMITER ;