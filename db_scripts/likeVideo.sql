DELIMITER //

DROP PROCEDURE IF EXISTS likeVideo //

CREATE PROCEDURE likeVideo (IN uName varchar(255), IN vId INT)
BEGIN
INSERT INTO Likes(idUser, idVideo) VALUES ((SELECT idUser FROM Users WHERE userName = uName), vId);
END//

DELIMITER ;