DELIMITER //

DROP PROCEDURE IF EXISTS writeComment //

CREATE PROCEDURE writeComment(IN uName varchar(255), IN videoId INT, IN commentBody varchar(255))
BEGIN
INSERT INTO Comments (idUser, idVideo, commentText) VALUES ((SELECT idUser FROM Users WHERE userName = uName), videoId, commentBody);
END //

DELIMITER ;