DELIMITER //

DROP PROCEDURE IF EXISTS getUserInfo //

CREATE PROCEDURE getUserInfo (IN uname varchar(255))
BEGIN
SELECT * FROM Users WHERE userName = uname;
END//

DELIMITER ;