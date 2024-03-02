CREATE TABLE Usuarios (
    UsuarioID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE,
    FechaRegistro DATE NOT NULL
);

CREATE TABLE Bocadillos (
    BocadilloID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL
);

CREATE TABLE Ingredientes (
    IngredienteID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Descripción TEXT
);

CREATE TABLE RegistrosDeConsumo (
    RegistroID INTEGER PRIMARY KEY AUTOINCREMENT,
    UsuarioID INTEGER,
    BocadilloID INTEGER,
    FechaConsumo DATE NOT NULL,
    FOREIGN KEY (UsuarioID) REFERENCES Usuarios(UsuarioID),
    FOREIGN KEY (BocadilloID) REFERENCES Bocadillos(BocadilloID)
);

CREATE TABLE BocadilloIngredientes (
    BocadilloID INTEGER,
    IngredienteID INTEGER,
    Cantidad TEXT,
    FOREIGN KEY (BocadilloID) REFERENCES Bocadillos(BocadilloID),
    FOREIGN KEY (IngredienteID) REFERENCES Ingredientes(IngredienteID),
    PRIMARY KEY (BocadilloID, IngredienteID)
);
