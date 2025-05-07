from flask import Flask, render_template, request, send_file
import pandas as pd
import joblib

app = Flask(__name__)
model = joblib.load('model/model.joblib')

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

    # Check for missing required columns
    missing_cols = [col for col in required_features if col not in df.columns]
    if missing_cols:
        return f"Error: Missing columns in uploaded file: {missing_cols}", 400

    # Predict using real model
    prediction = model.predict(df[required_features])
    df["Predicted Number of Bugs"] = prediction

    output_path = "predicted_results.csv"
    df.to_csv(output_path, index=False)

    # Pass DataFrame as a single HTML table string (not a list)
    return render_template(
        "result.html",
        table=df.to_html(classes="table-auto w-full", index=False, border=0),
        csv_download_link="/download"
    )


@app.route("/download")
def download():
    return send_file("predicted_results.csv", as_attachment=True)

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

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/jenkins-auto-predict')
def jenkins_auto_predict():
    try:
        df = pd.read_csv("uploads/metrics_from_jenkins.csv")
        predictions = model.predict(df)
        df["Predicted Bugs"] = predictions
        return render_template("result.html", table=df.to_html(classes="table", index=False))
    except Exception as e:
        return f"Error reading Jenkins prediction file: {e}"