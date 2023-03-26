DELIMITER //

DROP PROCEDURE IF EXISTS writeComment //

CREATE PROCEDURE writeComment(IN userId INT, IN videoId INT, IN commentBody varchar(255))
BEGIN
INSERT INTO Comments (idUser, idVideo, commentText) VALUES (userId, videoId, commentBody);
END //

DELIMITER ;