from datetime import datetime
import codecs
import sqlite3

def load_tracks_from_file(cursor):
    data = codecs.open('unique_tracks.txt', 'r', encoding='iso-8859-2')
    records = []
    for line in data.read().split('\n')[:-1]:
        row = line.split('<SEP>', -1)
        try:
            records.append({'song_id': row[1], 'singer': row[2], 'song_title': row[3]})
        except Exception:
            records.append({'song_id': row[1], 'singer': row[2], 'song_title': ''})
    cursor.executemany("INSERT OR REPLACE INTO tracks (song_id, singer, song_title) VALUES (:song_id, :singer, :song_title)", records)

def insert_into_dates(cursor):
    records = []
    i = 1
    for year in range(2000, 2018):
        for month in range(1, 13):
            records.append({'id': i, 'year': year, 'month': month })
            i += 1
    sql_command = "INSERT OR REPLACE INTO dates (id, year, month) VALUES (:id, :year, :month)"
    cursor.executemany(sql_command, records)

def convert_data(line):
    row = line.rstrip('\n').split('<SEP>')
    date = datetime.utcfromtimestamp(int(row[2]))
    return { 'listener_id': row[0], 'song_id': row[1], 'date_id': 12*(date.year-2000)+date.month }

def split_data(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def insert_into_samples(cursor, records):
    sql_command = "INSERT OR REPLACE INTO demo (listener_id, song_id, date_id) VALUES (:listener_id, :song_id, :date_id)"
    cursor.executemany(sql_command, records)

def load_samples_data_from_file(cursor):
    data = open('triplets_sample_20p.txt', 'r')
    for l in split_data(data.readlines(), 1000000):
        insert_into_samples(cursor, [convert_data(item) for item in l])

# Create database in RAM
db = sqlite3.connect(':memory:')
cursor = db.cursor()

# Create tracks table
cursor.execute('''
CREATE TABLE tracks (
  song_id     TEXT PRIMARY KEY,
  singer      TEXT DEFAULT NULL,
  song_title       TEXT DEFAULT NULL
)
''')
# Load data to table
load_tracks_from_file(cursor)
# Create dates table
cursor.execute('''
CREATE TABLE dates (
  id     INTEGER PRIMARY KEY,
  year   INTEGER NOT NULL,
  month  INTEGER NOT NULL
)
''')
# Load content to date's table
insert_into_dates(cursor)
# Create samples table
cursor.execute('''
CREATE TABLE demo (
  ID                INTEGER PRIMARY KEY AUTOINCREMENT,
  listener_id           TEXT NOT NULL,
  song_id           TEXT NOT NULL,
  date_id           INTEGER NOT NULL
)
''')
# Loat samples to table
load_samples_data_from_file(cursor)

# ex1
for row in cursor.execute('''
SELECT tracks.song_title, tracks.singer, sub.total_count
FROM (
    SELECT song_id, COUNT(song_id) AS total_count
    FROM demo
    GROUP BY song_id
    ORDER BY total_count DESC
    LIMIT 10
) sub
INNER JOIN tracks ON (tracks.song_id = sub.song_id)
ORDER BY sub.total_count DESC;
'''):
    print(' '.join([str(i) for i in row]))
print()
# ex2
for row in cursor.execute('''
SELECT listener_id, COUNT(DISTINCT song_id) AS counter
FROM demo
GROUP BY listener_id
ORDER BY counter DESC
LIMIT 10;
'''):
    print(' '.join([str(i) for i in row]))
print()
# ex3
for row in cursor.execute('''
SELECT t.singer, COUNT(t.singer) AS counter
FROM tracks AS t
INNER JOIN demo AS l ON (l.song_id = t.song_id)
GROUP BY t.singer
ORDER BY counter DESC
LIMIT 1;
'''):
    print(' '.join([str(i) for i in row]))
print()
# ex4
for row in cursor.execute('''
SELECT (((date_id + 11) % 12) + 1) AS date_month, COUNT(date_id)
FROM demo
GROUP BY date_month
ORDER BY date_month ASC;
'''):
    print(' '.join([str(i) for i in row]))
print()
# ex5
for row in cursor.execute('''
SELECT listener_id FROM demo
WHERE
  song_id IN (
    SELECT song_id FROM demo
    WHERE
      song_id IN (
        SELECT song_id FROM tracks
        WHERE
          singer = 'Queen'
      )
    GROUP BY song_id
    ORDER BY COUNT(song_id) DESC
    LIMIT 3
  )
GROUP BY listener_id
HAVING COUNT(DISTINCT song_id) = 3
ORDER BY listener_id ASC
LIMIT 10;
'''):
    print(' '.join([str(i) for i in row]))
