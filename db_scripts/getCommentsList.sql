DELIMITER //

DROP PROCEDURE IF EXISTS getCommentsList//

CREATE PROCEDURE getCommentsList (IN videoId INT)
BEGIN
SELECT * FROM Comments WHERE idVideo = videoId;
END//

DELIMITER ;