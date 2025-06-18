import random

def classify_image(image_path):
    labels = ["Normal Skin", "Rash", "Pink Eye", "Minor Cut"]
    return random.choice(labels)
