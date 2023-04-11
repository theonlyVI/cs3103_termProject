DELIMITER //

DROP PROCEDURE IF EXISTS deleteComment //

CREATE PROCEDURE deleteComment (IN commentId INT)
BEGIN
DELETE FROM Comments WHERE idComment = commentId;
END //

DELIMITER ;