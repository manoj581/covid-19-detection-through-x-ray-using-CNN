from flask import Flask, request, jsonify 
from ludwig.api import LudwigModel
import pandas as pd

# creating a Flask application
app = Flask(__name__)

# Load the model
model = LudwigModel.load('model.h5')

# creating predict url and only allowing post requests.
@app.route('/predict', methods=['POST'])
def predict():
    # Get data from Post request
    data = request.get_json()

    # Make prediction
    prediction = model.predict([prepare(data)], verbose=0)

    print(prediction)
    # returning the predictions as json
    if (prediction[0][0] > prediction[0][1]):
        return jsonify("covid")
    else:
        return jsonify("normal")


def prepare(data):
    testdata = []
    image = cv2.imread(data)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    testdata.append(image);
    testdata = np.array(testdata) / 255.0
    return testdata
if __name__ == '__main__':
    app.run(port=3000, debug=True)