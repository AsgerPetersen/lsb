import sqlite3
import csv
import sys

def importfile(dbfile, csvfile, kontonummer):
    con = sqlite3.connect( dbfile )
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS postering (id INTEGER PRIMARY KEY AUTOINCREMENT, kontonummer TEXT, dato TEXT, tekst TEXT, beloeb REAL, saldo REAL, kategoriid INT)')
    cur.execute('CREATE TABLE IF NOT EXISTS konto (kontonummer TEXT PRIMARY KEY, tekst TEXT)')

    with open(csvfile) as fr:
        csvreader = csv.reader(fr, delimiter=';', quotechar='"')
        # for line in csvreader:
        #     post = { 'kontonummer': kontonummer,
        #              'dato': line[0],
        #              'tekst': line[2],
        #              'beloeb': line[3],
        #              'saldo': line[4]
        #             }

        cur.executemany('INSERT INTO postering (kontonummer,dato,tekst,beloeb,saldo) VALUES(?,?,?,?,?)', csvreader)

def main():
    dbfile  = '/Users/asger/Code/lsb/data/posteringer.db' #sys.argv[1]
    csvfile = '/Users/asger/Code/lsb/data/0400_4011892294_Loenkonto_export.csv' #sys.argv[2]
    konto   = 'konto' #sys.argv[3]

    importfile(dbfile, csvfile, konto)

if __name__ == '__main__':
    main()
