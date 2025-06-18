import tensorflow as tf
import numpy as np
from PIL import Image

# Load labels
with open("model/labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

# Load model once when the file is imported
interpreter = tf.lite.Interpreter(model_path="model/model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def classify_image(image_path):
    # Load and preprocess the image
    img = Image.open(image_path).convert('RGB').resize((224, 224))
    img = np.array(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()

    # Get prediction
    output = interpreter.get_tensor(output_details[0]['index'])[0]
    predicted_index = np.argmax(output)
    return labels[predicted_index]
