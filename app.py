from flask import Flask, render_template, request, send_file
import pandas as pd
import joblib
import os
from metric_extractor import extract_metrics  # Correct import spelling

app = Flask(__name__)
model = joblib.load('model/model.joblib')

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return "No file uploaded", 400
    file = request.files["file"]
    if file.filename == "":
        return "Empty file name", 400

    df = pd.read_csv(file)
    required_features = [
        'TCLOC', 'LLOC', 'TNA', 'NM',
        'PUA', 'TLLOC', 'NLE', 'TNLPM',
        'TLOC', 'NLPM', 'NLM', 'TNLM',
        'NOI', 'TNOS', 'NOS', 'NL'
    ]
    missing_cols = [col for col in required_features if col not in df.columns]
    if missing_cols:
        return f"Error: Missing columns in uploaded file: {missing_cols}", 400

    prediction = model.predict(df[required_features])
    df["Predicted Number of Bugs"] = prediction

    output_path = "predicted_results.csv"
    df.to_csv(output_path, index=False)

    return render_template(
        "result.html",
        table=df.to_html(classes="table-auto w-full", index=False, border=0),
        csv_download_link="/download"
    )

@app.route("/analyze", methods=["POST"])
def analyze():
    uploaded_files = request.files.getlist("files")
    for file in uploaded_files:
        if file.filename:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    metrics_csv = os.path.join(UPLOAD_FOLDER, "metrics.csv")
    extract_metrics(UPLOAD_FOLDER, metrics_csv)
    df = pd.read_csv(metrics_csv)
    required_features = [
        'TCLOC', 'LLOC', 'TNA', 'NM',
        'PUA', 'TLLOC', 'NLE', 'TNLPM',
        'TLOC', 'NLPM', 'NLM', 'TNLM',
        'NOI', 'TNOS', 'NOS', 'NL'
    ]
    missing_cols = [col for col in required_features if col not in df.columns]
    if missing_cols:
        return f"Error: Missing columns in metrics: {missing_cols}", 400
    prediction = model.predict(df[required_features])
    df["Predicted Number of Bugs"] = prediction
    output_path = os.path.join(UPLOAD_FOLDER, "predicted_results.csv")
    df.to_csv(output_path, index=False)
    return render_template(
        "result.html",
        table=df.to_html(classes="table-auto w-full", index=False, border=0),
        csv_download_link="/download"
    )

@app.route("/download")
def download():
    return send_file(os.path.join(UPLOAD_FOLDER, "predicted_results.csv"), as_attachment=True)

@app.route("/generate-sample-csv")
def generate_sample_csv():
    sample_data = {
        'TCLOC': [50],
        'LLOC': [40],
        'TNA': [3],
        'NM': [2],
        'PUA': [5],
        'TLLOC': [100],
        'NLE': [1],
        'TNLPM': [6],
        'TLOC': [90],
        'NLPM': [3],
        'NLM': [1],
        'TNLM': [2],
        'NOI': [4],
        'TNOS': [2],
        'NOS': [3],
        'NL': [6]
    }
    df = pd.DataFrame(sample_data)
    df.to_csv("sample_input.csv", index=False)
    return send_file("sample_input.csv", as_attachment=True)

@app.route('/jenkins-auto-predict')
def jenkins_auto_predict():
    try:
        df = pd.read_csv("uploads/metrics_from_jenkins.csv")
        predictions = model.predict(df)
        df["Predicted Bugs"] = predictions
        return render_template("result.html", table=df.to_html(classes="table", index=False))
    except Exception as e:
        return f"Error reading Jenkins prediction file: {e}"

if __name__ == "__main__":
    app.run(debug=True)
