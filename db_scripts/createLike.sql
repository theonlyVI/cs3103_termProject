DROP TABLE IF EXISTS Likes;
CREATE TABLE Likes (
  idLike           INT          NOT NULL AUTO_INCREMENT,
  idUser           INT          NOT NULL,
  idVideo          INT          NOT NULL,
  PRIMARY KEY (idLike),
  FOREIGN KEY (idUser)  REFERENCES Users (idUser),
  FOREIGN KEY (idVideo) REFERENCES Videos (idVideo)
);