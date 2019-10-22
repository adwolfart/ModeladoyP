CREATE DATABASE Practica6;
USE Practica6;
CREATE TABLE Jugador(
    pk_id_jugador INT AUTO_INCREMENT PRIMARY KEY  ,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Partida(
    pk_id_partida INTEGER AUTO_INCREMENT PRIMARY KEY ,
    tablero_cifrado VARCHAR(255) NOT NULL,
    fk_id_jugador_en_turno INTEGER,
    fk_id_creador INTEGER NOT NULL,
    fk_id_oponente INTEGER NOT NULL,
    resultado ENUM('gana','pierde','empate')
);

ALTER TABLE Partida
ADD FOREIGN KEY (fk_id_jugador_en_turno) REFERENCES Jugador(pk_id_jugador);
ALTER TABLE Partida
ADD FOREIGN KEY (fk_id_creador) REFERENCES Jugador(pk_id_jugador);
ALTER TABLE Partida
ADD FOREIGN KEY (fk_id_oponente) REFERENCES Jugador(pk_id_jugador);
