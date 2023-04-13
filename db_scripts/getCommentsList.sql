DELIMITER //

DROP PROCEDURE IF EXISTS getCommentsList//

CREATE PROCEDURE getCommentsList (IN videoId INT)
BEGIN
SELECT * FROM Comments, Users WHERE idVideo = videoId AND Users.idUser =  Comments.idUser;
END//

DELIMITER ;