from database import update_album_tags, update_album_ratings, update_song_ratings, read_album_tags

update_album_tags('1', '2', '3')
update_album_tags('1', '2', '3')
update_album_tags('3', '6', '5')
update_album_ratings('1', '2', 6)
update_album_ratings('1', '2', 5)
update_song_ratings('1', '4', 3)
update_song_ratings('1', '4', 9)
print read_album_tags()
