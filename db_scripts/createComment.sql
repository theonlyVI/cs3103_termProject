DROP TABLE IF EXISTS Comments;
CREATE TABLE Comments (
  idComment        INT          NOT NULL AUTO_INCREMENT,
  commentText      varchar(255) NOT NULL,
  idUser           INT          NOT NULL,
  idVideo          INT          NOT NULL,
  PRIMARY KEY (idComment),
  FOREIGN KEY (idUser)  REFERENCES Users (idUser),
  FOREIGN KEY (idVideo) REFERENCES Videos (idVideo)
);