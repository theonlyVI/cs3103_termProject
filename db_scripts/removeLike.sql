DELIMITER //

DROP PROCEDURE IF EXISTS removeLike //

CREATE PROCEDURE removeLike (IN uName varchar(255), IN vId INT)
BEGIN
DELETE FROM Likes WHERE idUser IN (SELECT idUser FROM Users WHERE userName = uName) AND idVideo = vId;
END//

DELIMITER ;