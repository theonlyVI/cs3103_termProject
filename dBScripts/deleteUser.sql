DELIMITER //

DROP PROCEDURE IF EXISTS deleteUser //

CREATE PROCEDURE deleteUser(IN uName varchar(255))
BEGIN
DELETE FROM Comments WHERE idUser IN (SELECT idUser FROM Users WHERE userName = uName);
DELETE FROM Likes WHERE idUser IN (SELECT idUser FROM Users WHERE userName = uName);
DELETE FROM Videos WHERE idUser IN (SELECT idUser FROM Users WHERE userName = uName);
DELETE FROM Users WHERE userName = uName;
END//

DELIMITER ;