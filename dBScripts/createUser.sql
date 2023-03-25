DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
  idUser       INT          NOT NULL AUTO_INCREMENT,
  userName     varchar(256) NOT NULL,
  pWord        varchar(256) NOT NULL,
  PRIMARY KEY (idUser)
);