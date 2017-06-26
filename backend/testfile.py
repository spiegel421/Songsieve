from database import update_album_tags, update_album_ratings, update_song_ratings, read_album_tags
from tagmatrix import convert_to_matrix, convert_to_npmi, autoencode, find_distance_matrix, rank_distance_matrix
from random import randrange

#for i in range(1000):
#  update_album_tags(str(randrange(100)), "A" + str(randrange(20)), "T" + str(randrange(100)))
matrix = convert_to_matrix(read_album_tags())
npmi_matrix = convert_to_npmi(matrix)
encoded_space = autoencode(npmi_matrix)
distance_matrix = find_distance_matrix(matrix, encoded_space)
print rank_distance_matrix(distance_matrix)
