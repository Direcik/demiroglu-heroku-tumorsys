import os
import numpy as np
from PIL import Image
import cv2
from keras.models import load_model
from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
model = load_model('BrainTumor10EpochsCategorical.h5')

def get_className(classNo):
    if classNo == 0:
        return 'BEYİNDE TÜMÖR YOK'
    elif classNo == 1:
        return 'BEYİNDE TÜMÖR MEVCUT'

def getResult(img):
    image = cv2.imread(img)
    image = Image.fromarray(image, 'RGB')
    image = image.resize((64,64))
    image = np.array(image)
    input_img = np.expand_dims(image, axis = 0)
    result = np.argmax(model.predict(input_img), axis = -1)
    return result

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/braintumordetection")
def braintumordetection():
    return render_template("braintumordetection.html")

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        value = getResult(file_path)
        result = get_className(value)
        return result

