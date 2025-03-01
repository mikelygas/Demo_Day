# Import dependencies
import numpy as np
import pandas as pd
import json
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    Response)
from flask_mysqldb import MySQL
from joblib import load
from sklearn.datasets import load_breast_cancer



# Set up Flask
app = Flask(__name__)


#MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'cookies25'
app.config['MYSQL_DB'] = 'breastcancer'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

# home route
@app.route("/")
def index():
    """Renders homepage"""

    return render_template("index.html")


# vizualisations/tableau route
@app.route("/story")
def story():
    """Renders visualizations page"""

    return render_template("story.html")


@app.route("/cases")
def cases():
    """Renders case studies page"""

    return render_template("cases.html")


@app.route("/calculator")
def calc():
    """Renders demo page"""

    return render_template("calculator.html")

@app.route("/features/<patientID>")
def features(patientID):
    """Returns list of features for given patient ID"""

    # Create list of feature names
    feature_names = [
        "Radius (worst)",
        "Texture (worst)",
        "Perimeter (worst)",
        "Area (worst)",
        "Smoothness (worst)",
        "Compactness (worst)",
        "Concavity (worst)",
        "Concave points (worst)",
        "Symmetry (worst)",
        "Fractal dimension (worst)"]

    row = int(patientID) - 19000

    # Load dataset from sklearn and set X to feature array
    X = load_breast_cancer().data
    feature_values = X[row]

    # Select only features to be displayed
    feature_values = feature_values[20:]

    # Create dictionary of keys feature names and values
    features_dict = dict(zip(feature_names, feature_values))

    return jsonify(features_dict)


@app.route("/analyze/<patientID>")
def analyze(patientID):
    """Analyzes data for given patient using machine learning model
    and returns diagnosis"""

    # Translate patient ID to row
    row = (int(patientID) - 19000)

    # Load features, model, and scaler
    X = load_breast_cancer().data
    model = load("cancer_model.joblib")
    scaler = load("scaler.out")

    # Get features for selected row and scale
    row = np.array([row])
    feature_values = X[row]
    feature_values = scaler.transform(feature_values)

    # Predict diagnosis
    prediction = model.predict(feature_values)
    if prediction == 0:
        diagnosis = "Benign"
    else:
        diagnosis = "Malignant"

    return jsonify(diagnosis)

@app.route('/age-pivot')
def age_pivot():
        cur = mysql.connection
        df = pd.read_sql('SELECT * FROM age_pivot', cur)

        jsonfiles = json.loads(df.to_json(orient='records'))

        return jsonify(jsonfiles)

@app.route('/race-pivot')
def race_pivot():
        cur = mysql.connection
        df = pd.read_sql('SELECT * FROM race_pivot', cur)

        jsonfiles = json.loads(df.to_json(orient='records'))

        return jsonify(jsonfiles)


if __name__ == "__main__":
    app.run(debug=False, port=8000, host="localhost", threaded=True)
