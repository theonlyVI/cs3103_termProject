DELIMITER //

DROP PROCEDURE IF EXISTS getLikeCount//

CREATE PROCEDURE getLikeCount (IN videoId INT)
BEGIN
SELECT COUNT(idLike) as likeCount, videoId FROM Likes WHERE idVideo = videoId;
END//

DELIMITER ;
