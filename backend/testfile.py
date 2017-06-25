from database import update_album_tags, update_album_ratings, update_song_ratings, read_album_tags
from tagmatrix import convert_to_matrix, convert_to_npmi

update_album_tags('1', '2', '3')
update_album_tags('9', '2', '3')
update_album_tags('3', '6', '5')
update_album_ratings('1', '2', 6)
update_album_ratings('1', '2', 5)
update_song_ratings('1', '4', 3)
update_song_ratings('1', '4', 9)
matrix = convert_to_matrix(read_album_tags())
print matrix
print convert_to_npmi(matrix)
