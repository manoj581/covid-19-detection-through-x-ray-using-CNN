import numpy as np
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
import cv2
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
model=load_model('model.h5')
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:''@localhost/mydb'
db=SQLAlchemy(app)

class FileContents(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(300))
    data=db.Column(db.LargeBinary)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/upload',methods=['POST'])
def upload():
    file=request.files['inputFile']
    newFile=FileContents(name=file.filename, data=file.read())
    db.session.add(newFile)
    db.session.commit()
    return 'Saved'+file.filename


@app.route('/predict', methods=['POST'])
def predict():
    # Get data from Post request
    data = request.get_json()

    # Make prediction
    prediction = model.predict([prepare(data)], verbose=0)

    print(prediction)
    # returning the predictions as json
    if (prediction[0][0] > prediction[0][1]):
        output="covid"
    else:
        output="normal"

    return render_template('index.html', prediction_text='Employee Salary should be $ {}'.format(output))

def prepare(data):
    testdata = []
    image = cv2.imread(data)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    testdata.append(image);
    testdata = np.array(testdata) / 255.0
    return testdata


if __name__ == "__main__":
    app.run(debug=True)