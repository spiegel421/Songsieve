from database import *
from tagmatrix import *
from random import randrange

#for i in range(1000):
#  update_album_tags(str(randrange(100)), "A" + str(randrange(20)), "T" + str(randrange(100)))
matrix = convert_to_matrix(read_album_tags())
npmi_matrix = convert_to_npmi(matrix)
encoded_space = autoencode(npmi_matrix)
distance_matrix = find_distance_matrix(matrix, encoded_space)
print rank_distance_matrix(distance_matrix)
