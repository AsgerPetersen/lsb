import sqlite3
import csv
import sys

import codecs

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class LsbExportParser:
    def __init__(self, csvfile, kontonummer):
        self.file = csvfile
        self.kontonummer = kontonummer
        self.csvreader = UnicodeReader(csvfile, delimiter=';', quotechar='"',
            encoding='latin1')

    def next(self):
        row = self.csvreader.next()
        result = {}
        result['kontonummer']   = self.kontonummer
        result['dato']          = self._parse_date(row[0])
        result['tekst']         = row[2]
        result['beloeb']        = row[3]
        result['saldo']         = row[4]
        return result

    def __iter__(self):
        return self

    def _parse_date(self, lsbdate ):
        arr = lsbdate.split('-')
        return '{2}-{1}-{0}'.format(*arr)

class LsbImporter:
    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.connection = sqlite3.connect( dbfile )
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS postering ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'kontonummer TEXT, '
            'dato TEXT, '
            'tekst TEXT, '
            'beloeb REAL, '
            'saldo REAL, '
            'kategoriid INT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS konto ('
            'kontonummer TEXT PRIMARY KEY, '
            'tekst TEXT)')

    def importfile(self, filename, kontonummer ):
        with open(filename) as f:
            parser = LsbExportParser(f, kontonummer)
            for row in parser:
                self.cursor.execute('INSERT INTO postering (kontonummer,dato,tekst,beloeb,saldo) '
                    'VALUES(:kontonummer, :dato, :tekst, :beloeb, :saldo)', row)

    def db_datespans(self):
        self.cursor.execute('SELECT kontonummer, max(dato), min(dato) '
                                'FROM postering GROUP BY kontonummer')
        return {r[0]: {'maxdato': r[1], 'mindato': r[2]}
                for r in self.cursor.fetchall()}

    def commit(self):
        self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

def main():
    dbfile  = '/Users/asger/Code/lsb/data/posteringer.db' #sys.argv[1]
    csvfile = '/Users/asger/Code/lsb/data/0400_4011892294_Loenkonto_export.csv' #sys.argv[2]
    konto   = 'konto' #sys.argv[3]

    i = LsbImporter(dbfile)
    print i.db_datespans()

if __name__ == '__main__':
    main()
