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
  "tag varchar(20) NOT NULL );")

# Same with rating albums: the user, album, and rating are stored.
TABLES['album_ratings'] = (
  "CREATE TABLE album_ratings( "
  "user varchar(20) NOT NULL, "
  "album varchar(100) NOT NULL, "
  "rating int(2) NOT NULL );")

# Same as above, only with songs, not albums.
TABLES['song_ratings'] = (
  "CREATE TABLE song_ratings( "
  "user varchar(20) NOT NULL, "
  "song varchar(100) NOT NULL, "
  "rating int(2) NOT NULL );")

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

cursor.close()
cnx.close()

# Allows users to update the album tags table.
def update_album_tags(user, album, tag):
  cnx = mysql.connector.connect(user='root', password='Reverie42')
  cursor = cnx.cursor()
  cnx.database = DB_NAME
  
  check_exists_already = ("SELECT EXISTS(SELECT 1 FROM album_tags "
                          "WHERE user = %s AND album = %s AND tag = %s) ")
  
  add_album_tag = ("INSERT INTO album_tags "
             "(user, album, tag) "
             "VALUES (%s, %s, %s); ")
  
  data_album_tag = (user, album, tag)
  
  if cursor.execute(check_exists_already, data_album_tag) == 0:
    cursor.execute(add_album_tag, data_album_tag)
    cnx.commit()
  
  cursor.close()
  cnx.close()

# Allows users to update the album ratings table.
def update_album_ratings(user, album, rating):
  cnx = mysql.connector.connect(user='root', password='Reverie42')
  cursor = cnx.cursor()
  cnx.database = DB_NAME
  
  add_album_rating = ("INSERT INTO album_ratings "
             "(user, album, rating) "
             "VALUES (%s, %s, %s); ")
  
  data_album_rating = (user, album, rating)
  
  cursor.execute(add_album_rating, data_album_rating)
  cnx.commit()
  
  cursor.close()
  cnx.close()
  
# Allows users to update the song ratings table.
def update_song_ratings(user, song, rating):
  cnx = mysql.connector.connect(user='root', password='Reverie42')
  cursor = cnx.cursor()
  cnx.database = DB_NAME
  
  add_song_rating = ("INSERT INTO song_ratings "
             "(user, song, rating) "
             "VALUES (%s, %s, %s); ")
  
  data_song_rating = (user, song, rating)
  
  cursor.execute(add_song_rating, data_song_rating)
  cnx.commit()
  
  cursor.close()
  cnx.close()
