# Establishes, in binary fashion, whether each album has each tag based on PMI values and auto-encoding.
import numpy as np
import pandas as pd

def convert_to_matrix(album_tag_dict):
  return pd.DataFrame(album_tag_dict).T.fillna(0)
