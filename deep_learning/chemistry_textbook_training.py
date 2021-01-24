#!/usr/bin/env python3.7

import os
import sys
import string
import shutil 

import numpy as np

import bs4

import tensorflow as tf

from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import preprocessing
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

dir_path = os.path.dirname(os.path.abspath(__file__))

@tf.keras.utils.register_keras_serializable()
def simple_standardization(input_data):
  lowercase = tf.strings.lower(input_data)
  return lowercase

def vectorize_text(text, label):
  text = tf.expand_dims(text, -1)
  return vectorize_layer(text), label

labels = ["biological", "organic", "inorganic", "physical"]

nsmall = 100 

if os.path.exists(os.path.join("data", "train")):
    shutil.rmtree(os.path.join("data", "train"))
if os.path.exists(os.path.join("data", "test")):
    shutil.rmtree(os.path.join("data", "test"))

for l in labels:
    os.makedirs(os.path.join("data","train",l))
    os.makedirs(os.path.join("data","test",l))
    with open(os.path.join("data", "{}.txt".format(l))) as f:
        text = np.asarray(f.read().lower().translate(str.maketrans('', '', string.punctuation)).split())
    nlarge = len(text)
    text = text[:nlarge-nlarge%nsmall]
    text = text.reshape(-1, nsmall)
    text_train = text[0::2]
    text_test  = text[1::2]
    for i, s in enumerate(text_train):
        with open(os.path.join("data", "train/{}/{}_{:04d}.txt".format(l, l, i)), "w") as f:
            f.write(" ".join(s))
    for i, s in enumerate(text_test):
        with open(os.path.join("data", "test/{}/{}_{:04d}.txt".format(l, l, i)), "w") as f:
            f.write(" ".join(s))

batch_size = 32
seed = 12345

raw_train_ds = tf.keras.preprocessing.text_dataset_from_directory(
    os.path.join("data", "train"),
    batch_size=batch_size, 
    validation_split=0.2,  
    subset='training', 
    seed=seed)
raw_val_ds = tf.keras.preprocessing.text_dataset_from_directory(
    os.path.join("data", "train"),
    batch_size=batch_size, 
    validation_split=0.2, 
    subset='validation', 
    seed=seed)
raw_test_ds = tf.keras.preprocessing.text_dataset_from_directory(
    os.path.join("data", "test"),
    batch_size=batch_size)

print(raw_train_ds.class_names)
for i in range(len(labels)):
    print(i, raw_train_ds.class_names[i])

max_features = 1000
embedding_dim = 8
epochs = 25

vectorize_layer = TextVectorization(
    standardize=simple_standardization,
    max_tokens=max_features,
    output_mode='int',
    )


# Make a text-only dataset (without labels), then call adapt
train_text = raw_train_ds.map(lambda x, y: x)
vectorize_layer.adapt(train_text)

train_ds = raw_train_ds.map(vectorize_text)
val_ds = raw_val_ds.map(vectorize_text)
test_ds = raw_test_ds.map(vectorize_text)

model = tf.keras.Sequential([
  layers.Embedding(max_features + 1, embedding_dim),
  layers.Dropout(0.2),
  layers.GlobalAveragePooling1D(),
  layers.Dropout(0.2),
  layers.Dense(len(labels))])

model.summary()
model.compile(loss=losses.SparseCategoricalCrossentropy(from_logits=True),
              optimizer='adam',
              metrics=['accuracy'])

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs)

loss, accuracy = model.evaluate(test_ds)
print("Loss: ", loss)
print("Accuracy: ", accuracy)

history_dict = history.history
history_dict.keys()

acc = history_dict['accuracy']
val_acc = history_dict['val_accuracy']
loss = history_dict['loss']
val_loss = history_dict['val_loss']

epochs = range(1, len(acc) + 1)

export_model = tf.keras.Sequential([
  vectorize_layer,
  model,
  layers.Activation('sigmoid')
])

export_model.compile(
    loss=losses.SparseCategoricalCrossentropy(from_logits=False), optimizer="adam", metrics=['accuracy']
)

# Test it with `raw_test_ds`, which yields raw strings
loss, accuracy = export_model.evaluate(raw_test_ds)
print(accuracy)

#[biological, inorganic, organic, physical]
examples = ["physical chemistry equilibria activation energy schrodinger equation"]

print(export_model.predict(examples))

export_model.save("classification_model")
