import os
import sys
import string
import shutil 

import numpy as np

import tensorflow as tf

@tf.keras.utils.register_keras_serializable()
def simple_standardization(input_data):
  lowercase = tf.strings.lower(input_data)
  return lowercase

dir_path = os.path.dirname(os.path.abspath(__file__))

model = tf.keras.models.load_model(os.path.join(dir_path, "classification_model"))

labels = ["chemistry/biological_chemistry",
          "chemistry/inorganic_chemistry", 
          "chemistry/organic_chemistry", 
          "chemistry/physical_chemistry"]

def predict_field(text):
  ilabel = np.argmax(model.predict([text])[0])
  return labels[ilabel]

print(predict_field("transition metal complex iron nickel cobalt inorganic"))
print(predict_field("physic schrodinger equation solve entropy boltzmann equilibria rate constants activation enthalpy"))
print(predict_field("genetics double helix dna rna atp"))
print(predict_field("alkane alkyne alkene carbonyl nucleophilic substitution mechanism"))
