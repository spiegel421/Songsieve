# Stores three tables: one for tags, one for album ratings, and one for song ratings.
import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'tags_ratings'

TABLES = {}
# Every time a user tags an album, the user, album, and tag are stored.
TABLES['album_tags'] = (
  "CREATE TABLE album_tags( "
  "user varchar(20) NOT NULL, "
  "album varchar(100) NOT NULL, "
  "tag varchar(20) NOT NULL ); ")

# Same with rating albums: the user, album, and rating are stored.
TABLES['album_ratings'] = (
  "CREATE TABLE album_ratings( "
  "user varchar(20) NOT NULL, "
  "album varchar(100) NOT NULL, "
  "rating int(2) NOT NULL ); ")

# Same as above, only with songs, not albums.
TABLES['song_ratings'] = (
  "CREATE TABLE song_ratings( "
  "user varchar(20) NOT NULL, "
  "song varchar(100) NOT NULL, "
  "rating int(2) NOT NULL ); ")

# Connects to mysql, defines a method for creating the database, and uses that method.
cnx = mysql.connector.connect(user='root', password='Reverie42')
cursor = cnx.cursor()

def create_database(cursor):
  try:
    cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
  except mysql.connector.Error as err:
     print "Failed creating database: {}".format(err)
     exit(1)

try:
    cnx.database = DB_NAME  
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print err
        exit(1)

for name, ddl in TABLES.iteritems():
    try:
        print "Creating table {}: ".format(name)
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print "already exists."
        else:
            print err.msg
    else:
        print "OK"

cnx.commit()
cursor.close()
cnx.close()

# Allows users to update the album tags table.
def update_album_tags(user, album, tag):
  cnx = mysql.connector.connect(user='root', password='Reverie42', buffered=True)
  cursor = cnx.cursor()
  cnx.database = DB_NAME
  
  check_exists = ("SELECT EXISTS(SELECT 1 FROM "
                  "album_tags WHERE user = %s "
                  "AND album = %s AND tag = %s); ")
  
  add_album_tag = ("INSERT INTO album_tags "
             "(user, album, tag) "
             "VALUES (%s, %s, %s); ")
  
  data = (user, album, tag)
  
  cursor.execute(check_exists, data)
  for item in cursor:
    exists = item[0]
  if exists == 0:
    cursor.execute(add_album_tag, data)
  
  cnx.commit()
  cursor.close()
  cnx.close()
  
# Reads the album tags table into a dictionary.
def read_album_tags():
  cnx = mysql.connector.connect(user='root', password='Reverie42', buffered=True)
  cursor = cnx.cursor()
  cnx.database = DB_NAME
  
  album_tag_dict = dict()
  
  cursor.execute("SELECT * FROM album_tags; ")
  for item in cursor:
    if (item[1], item[2]) in album_tag_dict:
      album_tag_dict[(item[1], item[2])] += 1
    else:
      album_tag_dict[(item[1], item[2])] = 0
  
  cnx.commit()
  cursor.close()
  cnx.close()
  
  return album_tag_dict
  
# Allows users to update the album ratings table.
def update_album_ratings(user, album, rating):
  cnx = mysql.connector.connect(user='root', password='Reverie42', buffered=True)
  cursor = cnx.cursor()
  cnx.database = DB_NAME
  
  check_rating_exists = ("SELECT EXISTS(SELECT * FROM "
                  "album_ratings WHERE user = %s "
                  "AND album = %s); ")
  
  check_rating_same =("SELECT EXISTS(SELECT * FROM "
                      "album_ratings WHERE user = %s "
                      "AND album = %s AND rating = %s); ")
  
  add_album_rating = ("INSERT INTO album_ratings "
             "(user, album, rating) "
             "VALUES (%s, %s, %s); ")
  
  change_album_rating = ("UPDATE album_ratings "
                         "SET rating = %s "
                         "WHERE user = %s AND album = %s; ")
  
  data = (user, album, rating)
  data_short = (user, album)
  data_change = (rating, user, album)
  
  cursor.execute(check_rating_exists, data_short)
  for item in cursor:
    exists = item[0]
  if exists == 0:
    cursor.execute(add_album_rating, data)
  else:
    cursor.execute(check_rating_same, data)
    for item in cursor:
      same = item[0]
    if same == 0:
      cursor.execute(change_album_rating, data_change)
  
  cnx.commit()
  cursor.close()
  cnx.close()
  
# Reads the album ratings table into a dictionary.
def read_album_ratings():
  cnx = mysql.connector.connect(user='root', password='Reverie42', buffered=True)
  cursor = cnx.cursor()
  cnx.database = DB_NAME
  
  album_rating_dict = dict()
  
  cursor.execute("SELECT * FROM album_ratings; ")
  for item in cursor:
    album_rating_dict[(item[0], item[1])] = item[2]
    
  cnx.commit()
  cursor.close()
  cnx.close()
  
  return album_rating_dict
  
# Allows users to update the song ratings table.
def update_song_ratings(user, song, rating):
  cnx = mysql.connector.connect(user='root', password='Reverie42', buffered=True)
  cursor = cnx.cursor()
  cnx.database = DB_NAME
  
  check_rating_exists = ("SELECT EXISTS(SELECT * FROM "
                  "song_ratings WHERE user = %s "
                  "AND song = %s); ")
  
  check_rating_same =("SELECT EXISTS(SELECT * FROM "
                      "song_ratings WHERE user = %s "
                      "AND song = %s AND rating = %s); ")
  
  add_song_rating = ("INSERT INTO song_ratings "
             "(user, song, rating) "
             "VALUES (%s, %s, %s); ")
  
  change_song_rating = ("UPDATE song_ratings "
                         "SET rating = %s "
                         "WHERE user = %s AND song = %s; ")
  
  data = (user, song, rating)
  data_short = (user, song)
  data_change = (rating, user, song)
  
  cursor.execute(check_rating_exists, data_short)
  for item in cursor:
    exists = item[0]
  if exists == 0:
    cursor.execute(add_song_rating, data)
  else:
    cursor.execute(check_rating_same, data)
    for item in cursor:
      same = item[0]
    if same == 0:
      cursor.execute(change_song_rating, data_change)
  
  cnx.commit()
  cursor.close()
  cnx.close()
  
# Reads the song ratings table into a dictionary.
def read_song_ratings():
  cnx = mysql.connector.connect(user='root', password='Reverie42', buffered=True)
  cursor = cnx.cursor()
  cnx.database = DB_NAME
  
  song_rating_dict = dict()
  
  cursor.execute("SELECT * FROM song_ratings; ")
  for item in cursor:
    song_rating_dict[(item[0], item[1])] = item[2]
    
  cnx.commit()
  cursor.close()
  cnx.close()
  
  return song_rating_dict
