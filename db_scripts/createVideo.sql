DROP TABLE IF EXISTS Videos;
CREATE TABLE Videos (
  idVideo          INT          NOT NULL AUTO_INCREMENT,
  videoPath        varchar(255) NOT NULL,
  uploadDate       varchar(45)  NOT NULL,
  idUser           INT          NOT NULL,
  videoTitle       varchar(100) NOT NULL,
  videoDescription varchar(255) NOT NULL,
  PRIMARY KEY (idVideo),
  FOREIGN KEY (idUser) REFERENCES Users (idUser)
);