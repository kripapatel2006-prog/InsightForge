from flask import Flask, render_template, request
import os
import uuid
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

# -----------------------------
# Configuration
# -----------------------------
UPLOAD_FOLDER = "uploads"
CHART_FOLDER = "static/charts"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)

# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Upload Page
# -----------------------------
@app.route("/upload-page")
def upload_page():
    return render_template("upload.html")


# -----------------------------
# Upload Dataset
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload():

    if "dataset" not in request.files:
        return "No file uploaded."

    file = request.files["dataset"]

    if file.filename == "":
        return "Please select a CSV file."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        return f"Error reading CSV: {e}"

    # -----------------------------
    # Dataset Statistics
    # -----------------------------
    rows = df.shape[0]
    columns = df.shape[1]

    missing_values = int(df.isnull().sum().sum())
    duplicates = int(df.duplicated().sum())

    column_names = df.columns.tolist()
    preview = df.head(10)

    # -----------------------------
    # Extra Information
    # -----------------------------
    filename = file.filename

    memory_usage = round(
        df.memory_usage(deep=True).sum() / 1024,
        2
    )

    numeric_columns = len(
        df.select_dtypes(include="number").columns
    )

    categorical_columns = len(
        df.select_dtypes(include="object").columns
    )

    # -----------------------------
    # AI Insights
    # -----------------------------
    insights = []

    if missing_values == 0:
        insights.append("The dataset has no missing values.")
    else:
        insights.append(f"The dataset contains {missing_values} missing values.")

    if duplicates == 0:
        insights.append("No duplicate records were found.")
    else:
        insights.append(f"The dataset contains {duplicates} duplicate records.")

    if numeric_columns > categorical_columns:
        insights.append(
            "The dataset is primarily numerical and is suitable for statistical analysis and machine learning."
        )
    else:
        insights.append(
            "The dataset contains more categorical features and is suitable for classification or business analysis."
        )

    insights.append(
        f"The dataset contains {rows} records and {columns} features."
    )

    # -----------------------------
    # Generate Bar Chart
    # -----------------------------
    chart_file = None

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        plt.figure(figsize=(8,5))

        df[numeric_cols[0]].value_counts().plot(kind="bar")

        plt.title(f"{numeric_cols[0]} Distribution")
        plt.xlabel(numeric_cols[0])
        plt.ylabel("Count")

        chart_file = f"{uuid.uuid4().hex}.png"

        chart_path = os.path.join(CHART_FOLDER, chart_file)

        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()

    # -----------------------------
    # Report Page
    # -----------------------------
    return render_template(
        "report.html",
        rows=rows,
        columns=columns,
        missing_values=missing_values,
        duplicates=duplicates,
        column_names=column_names,
        tables=preview.to_html(classes="table table-striped", index=False),
        filename=filename,
        memory_usage=memory_usage,
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        insights=insights,
        chart_file=chart_file
    )


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)