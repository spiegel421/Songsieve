# Establishes, in binary fashion, whether each album has each tag based on PMI values and auto-encoding.
import numpy as np
import pandas as pd
import copy

# Converts dictionaries to labeled matrices, using pandas's DataFrame class.
def convert_to_matrix(album_tag_dict):
  return pd.DataFrame(album_tag_dict).T.fillna(0)

# Generates matrix of NPMI values from matrix of counts.
def convert_to_npmi(count_matrix):
  npmi_matrix = copy.copy(count_matrix)
  
  for row in range(len(count_matrix.values)):
    for col in range(len(count_matrix.values[0])):
      entry = float(count_matrix.values[row][col])
      if entry == 0:
        npmi_matrix.values[row][col] = -1.0
        continue
      else:
        prob_con = entry / count_matrix.values.sum()
        if prob_con == 1.0:
          npmi_matrix.values[row][col] = 1.0
          continue
        else:
          prob_row = entry / count_matrix.values.sum(axis=0)[row]
          prob_col = entry / count_matrix.values.sum(axis=1)[col]
          npmi_value = -1.0 * np.log(prob_con / (prob_row * prob_col)) / np.log(prob_con)
          npmi_matrix.values[row][col] = npmi_value
          
  return npmi_matrix
