# Establishes, in binary fashion, whether each album has each tag based on PMI values and autoencoding.
import numpy as np
import pandas as pd
import copy
from keras.layers import Input, Dense
from keras.models import Model
from sklearn import svm

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
          prob_row = entry / count_matrix.values.sum(axis=1)[row]
          prob_col = entry / count_matrix.values.sum(axis=0)[col]
          npmi_value = -1.0 * np.log(prob_con / (prob_row * prob_col)) / np.log(prob_con)
          npmi_matrix.values[row][col] = npmi_value
          
  return npmi_matrix

# Auto-encodes NPMI matrix into 20 dimensions, using five-fold cross validation.
def autoencode(npmi_matrix):
  original_dim = len(npmi_matrix.values[0])
  encoding_dim = 20
  
  input = Input(shape=(original_dim,))
  encoded = Dense(encoding_dim, activation='tanh')(input)
  decoded = Dense(original_dim, activation='tanh')(encoded)
  
  autoencoder = Model(input, decoded)
  encoder = Model(input, encoded)
  encoded_input = Input(shape=(encoding_dim,))
  decoder_layer = autoencoder.layers[-1]
  decoder = Model(encoded_input, decoder_layer(encoded_input))
  
  X = npmi_matrix.values
  autoencoder.compile(optimizer='sgd', loss='mean_squared_error')
  autoencoder.fit(X, X, validation_split=0.2, 
                  epochs=50, batch_size=10)
  
  encoded_space = pd.DataFrame(encoder.predict(npmi_matrix.values), index=npmi_matrix.index)
  return encoded_space

# Determines the distance of each album from each tag's hyperplane.
def find_distance_matrix(count_matrix, encoded_space):
  distance_matrix = copy.copy(count_matrix).T
  
  clf = svm.LinearSVC()
  for tag in distance_matrix.index:
    y = copy.copy(distance_matrix.loc[tag])
    y = [1 if item > 0 else 0 for item in y.values]
    clf.fit(encoded_space.values, y)
    distance_matrix.loc[tag] = clf.decision_function(encoded_space.values)
    
  return distance_matrix

# Ranks albums by distance from each tag's hyperplane.
def rank_distance_matrix(distance_matrix):
  sorted_by_distance = {}
  for tag in distance_matrix.index:
    sorted_by_distance[tag] = sorted(distance_matrix.columns, 
                                     key=lambda album: distance_matrix.loc[tag][album], 
                                     reverse=True)
    
  ranked_matrix = copy.copy(distance_matrix)
  for tag in distance_matrix.index:
    ranked_matrix.loc[tag] = [sorted_by_distance[tag].index(album) + 1 for album in distance_matrix.columns]
    
  return ranked_matrix

# Finds normalized discounted cumulative gain (NDCG) for each tag.
def find_ndcg_values(npmi_matrix, ranked_matrix):
  ndcg_values = {}
  rankings_dict = ranked_matrix.to_dict(orient='index')
  for tag in ranked_matrix.index:
    dcg = 0.0
    album_rankings = rankings_dict[tag]
    for album in album_rankings:
      dcg += npmi_matrix.loc[album][tag] / (np.log(album_rankings[album] + 1) / np.log(2))
      
    idcg = 0.0
    sorted_relevancies = sorted(npmi_matrix.T.loc[tag], reverse=True)
    for i in range(len(sorted_relevancies)):
      idcg += sorted_relevancies[i] / (np.log(i + 2) / np.log(2))
      
    ndcg_values[tag] = dcg / idcg
    
  return ndcg_values
