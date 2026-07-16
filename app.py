from flask import Flask, render_template, request, send_file
import os
import uuid
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

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

    # Dataset Statistics
    rows = df.shape[0]
    columns = df.shape[1]

    missing_values = int(df.isnull().sum().sum())
    duplicates = int(df.duplicated().sum())

    preview = df.head(10)

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
        insights.append(
            f"The dataset contains {missing_values} missing values."
        )

    if duplicates == 0:
        insights.append("No duplicate records were found.")
    else:
        insights.append(
            f"The dataset contains {duplicates} duplicate records."
        )

    if numeric_columns > categorical_columns:
        insights.append(
            "The dataset is primarily numerical and is suitable for statistical analysis and machine learning."
        )
    else:
        insights.append(
            "The dataset contains more categorical features and is suitable for business analysis."
        )

    insights.append(
        f"The dataset contains {rows} rows and {columns} columns."
    )

    # -----------------------------
    # Generate Chart
    # -----------------------------

    chart_file = None

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        plt.figure(figsize=(8, 5))

        df[numeric_cols[0]].value_counts().plot(kind="bar")

        plt.title(f"{numeric_cols[0]} Distribution")

        plt.tight_layout()

        chart_file = f"{uuid.uuid4().hex}.png"

        chart_path = os.path.join(
            CHART_FOLDER,
            chart_file
        )

        plt.savefig(chart_path)

        plt.close()

    # -----------------------------
    # Report
    # -----------------------------

    return render_template(

        "report.html",

        rows=rows,
        columns=columns,
        missing_values=missing_values,
        duplicates=duplicates,

        filename=filename,
        memory_usage=memory_usage,
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,

        insights=insights,

        chart_file=chart_file,

        tables=preview.to_html(
            classes="table table-striped",
            index=False
        )
    )


# -----------------------------
# Download PDF Report
# -----------------------------
@app.route("/download-report")
def download_report():

    pdf_file = "InsightForge_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(Paragraph("InsightForge - Dataset Analysis Report", styles["Title"]))
    story.append(Spacer(1, 20))

    # Date
    current_date = datetime.now().strftime("%d %B %Y, %I:%M %p")
    story.append(Paragraph(f"<b>Generated on:</b> {current_date}", styles["BodyText"]))
    story.append(Spacer(1, 20))

    # Dataset section
    story.append(Paragraph("<b>Dataset Information</b>", styles["Heading2"]))
    story.append(Paragraph("This report was generated automatically by InsightForge.", styles["BodyText"]))
    story.append(Spacer(1, 15))

    # AI Insights section
    story.append(Paragraph("<b>AI Insights</b>", styles["Heading2"]))
    story.append(Paragraph("• The dataset was successfully analyzed.", styles["BodyText"]))
    story.append(Paragraph("• Dataset statistics and visualizations are available on the web dashboard.", styles["BodyText"]))
    story.append(Paragraph("• InsightForge helps users quickly understand uploaded CSV datasets.", styles["BodyText"]))
    story.append(Spacer(1, 20))

    # Add chart if available
    chart_folder = "static/charts"

    if os.path.exists(chart_folder):
        chart_files = [f for f in os.listdir(chart_folder) if f.endswith(".png")]

        if chart_files:
            latest_chart = os.path.join(chart_folder, chart_files[-1])

            story.append(Paragraph("<b>Data Visualization</b>", styles["Heading2"]))
            story.append(Image(latest_chart, width=450, height=280))
            story.append(Spacer(1, 20))

    # Footer
    story.append(Paragraph("Generated using InsightForge", styles["Italic"]))
    story.append(Paragraph("Developed by Kripa Patel", styles["Italic"]))

    doc.build(story)

    return send_file(pdf_file, as_attachment=True)

# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)