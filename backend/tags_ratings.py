# Stores three tables: one for tags, one for album ratings, and one for song ratings.

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'tags_ratings'

TABLES = {}
TABLES['tags'] = (
  "CREATE TABLE tags( "
  "user varchar(20) NOT NULL, "
  "album varchar(100) NOT NULL, "
  "tag varchar(20) NOT NULL, "
  "PRIMARY KEY (user)); ")

TABLES['album_ratings'] = (
  "CREATE TABLE 'album_ratings'( "
  "'user' varchar(20) NOT NULL, "
  "'album' varchar(100) NOT NULL, "
  "'rating' int(2) NOT NULL, "
  "PRIMARY KEY ('user')); ")

TABLES['song_ratings'] = (
  "CREATE TABLE 'song_ratings'( "
  "'user' varchar(20) NOT NULL, "
  "'song' varchar(100) NOT NULL, "
  "'rating' int(2) NOT NULL, "
  "PRIMARY KEY ('user')); ")

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
