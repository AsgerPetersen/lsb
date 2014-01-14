lsb
===

Database
--------

Postering
---------
id          INT PRIMARY KEY AUTOINCREMENT
kontoid     INT
dato        TEXT
tekst       TEXT
beloeb      REAL
saldo       REAL
kategoriid  INT

kategori
--------
id          INT PRIMARY KEY AUTOINCREMENT
tekst       TEXT

overkategori
------------
id          INT PRIMARY KEY AUTOINCREMENT
tekst       TEXT

konto
-----------
id          INT PRIMARY KEY AUTOINCREMENT
tekst       TEXT
