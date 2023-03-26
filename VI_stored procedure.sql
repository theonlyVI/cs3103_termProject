DELIMITER //
DROP PROCEDURE IF EXISTS deleteComment //

CREATE PROCEDURE deleteComment(IN userIdIn INT, IN videoIdIn INT)
BEGIN
  DELETE FROM Comments WHERE idVideo = videoIdIn AND idUser = userIdIn;
END //

DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS likeVideo //

CREATE PROCEDURE likeVideo(IN userIdIn INT, IN videoIdIn INT)
BEGIN
  INSERT INTO Likes (idUser, idVideo) VALUES (userIdIn, videoIdIn); 
END //

DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS createUser //

CREATE PROCEDURE createUser(IN userNameIn VARCHAR(255))
BEGIN
  INSERT INTO Users (userName) VALUES (userNameIn); 
END //

DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS removeLike //

CREATE PROCEDURE removeLike(IN userIdIn INT, IN videoIdIn INT)
BEGIN
  DELETE FROM Likes WHERE idUser = userIdIn AND idVideo = videoIdIn; 
END //

DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS changeVideoDescription //

CREATE PROCEDURE changeVideoDescription(IN videoIdIn INT, IN vidDesIn VARCHAR(255))
BEGIN
  UPDATE Videos SET videoDescription = vidDesIn WHERE idVideo = videoIdIn; 
END //

DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS changeVideoTitle //

CREATE PROCEDURE changeVideoTitle(IN videoIdIn INT, IN titleIn VARCHAR(255))
BEGIN
  UPDATE Videos SET videoTitle = titleIn WHERE idVideo = videoIdIn; 
END //

DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS editComment //

CREATE PROCEDURE editComment(IN userIdIn INT, IN videoIdIn INT, IN commentIn VARCHAR(255))
BEGIN
  UPDATE Comments SET commentText = commentIn WHERE userIdIn = idUser AND idVideo = videoIdIn;
END //

DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS changePassword //

CREATE PROCEDURE changePassword(IN userIdIn INT, IN pwordIn VARCHAR(255))
BEGIN
  UPDATE Users SET pWord = MD5(pwordIn) WHERE idUser = userIdIn; 
END //

DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS changeUserName //

CREATE PROCEDURE changeUserName(IN userNameIn VARCHAR(255), IN userIdIn INT)
BEGIN
  UPDATE Users SET userName = userNameIn WHERE idUser = userIdIn; 
END //

DELIMITER ;


