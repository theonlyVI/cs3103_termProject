DELIMITER //

DROP PROCEDURE IF EXISTS getVideoList//

CREATE PROCEDURE getVideoList (IN uName varchar(255))
BEGIN
SELECT * FROM Videos WHERE idUser IN (SELECT idUser FROM Users WHERE userName = uName);
END//

DELIMITER ;