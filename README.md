lsb
===

Database
--------

```
Postering
---------
id          INT PRIMARY KEY AUTOINCREMENT
kontonummer TEXT
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
kontonummer TEXT PRIMARY KEY
tekst       TEXT
```
