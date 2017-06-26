from tags_ratings import *
from tagmatrix import *
from random import randrange

#for i in range(1000):
#  update_album_tags(str(randrange(100)), "A" + str(randrange(20)), "T" + str(randrange(100)))
matrix = convert_to_matrix(read_album_tags())
ppmi_matrix = convert_to_ppmi(matrix)
encoded_space = autoencode(ppmi_matrix)
distance_matrix = find_distance_matrix(matrix, encoded_space)
ranked_matrix = rank_distance_matrix(distance_matrix)
ndcg_values = find_ndcg_values(ppmi_matrix, ranked_matrix)
print ndcg_values
