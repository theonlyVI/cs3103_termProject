DELIMITER //

DROP PROCEDURE IF EXISTS getVideo//

CREATE PROCEDURE getVideo (IN videoName VARCHAR(255), IN videoId INT)
BEGIN 
SELECT * FROM Videos WHERE videoTitle LIKE Concat('%', @videoName, '%') OR idVideo = videoId;
END//

DELIMITER ;
