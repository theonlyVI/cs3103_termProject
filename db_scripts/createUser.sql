DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
  idUser       INT          NOT NULL AUTO_INCREMENT,
  userName     varchar(255) NOT NULL,
  pWord        varchar(255) NOT NULL,
  PRIMARY KEY (idUser)
);