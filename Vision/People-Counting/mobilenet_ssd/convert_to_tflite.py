import tensorflow as tf
from tensorflow.keras.models import load_model

model = load_model('./test/saved_model')

converter = tf.lite.TFLiteConverter.from_saved_model(model)
tflite_model = converter.convert()

with open("activity-lite.tflite", "wb") as f:
  f.write(tflite_model)

# Convert the model
#converter = tf.lite.TFLiteConverter.from_saved_model('./test/save_model') # path to the SavedModel directory
#tflite_model = converter.convert()

# Save the model.
#with open('model.tflite', 'wb') as f:
#  f.write(tflite_model)

