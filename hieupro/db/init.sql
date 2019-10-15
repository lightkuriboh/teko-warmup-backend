
CREATE DATABASE teko_first_project;
USE teko_first_project;
CREATE TABLE user(
   users_id INT NOT NULL AUTO_INCREMENT,
   username varchar(20) NOT NULL,
   password VARCHAR(50) NOT NULL,
   email VARCHAR(150) NOT NULL,
   privilege VARCHAR(150) NOT NULL,
   PRIMARY KEY ( users_id )
);