from flask import Flask, render_template, request, send_file
import os
import uuid
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

# --------------------------------------------------
# Configuration
# --------------------------------------------------

UPLOAD_FOLDER = "uploads"
CHART_FOLDER = "static/charts"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024   # 20 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# Upload Page
# --------------------------------------------------

@app.route("/upload-page")
def upload_page():
    return render_template("upload.html")


# --------------------------------------------------
# Upload Dataset
# --------------------------------------------------

@app.route("/upload", methods=["POST"])
def upload():

    if "dataset" not in request.files:
        return render_template(
            "error.html",
            message="No file was uploaded."
        )

    file = request.files["dataset"]

    if file.filename == "":
        return render_template(
            "error.html",
            message="Please choose a CSV file."
        )

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    try:
        df = pd.read_csv(filepath)

    except Exception:

        return render_template(
            "error.html",
            message="Unable to read the uploaded CSV file."
        )

    # ---------------------------------------
    # Dataset Statistics
    # ---------------------------------------

    rows = df.shape[0]
    columns = df.shape[1]

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicates = int(
        df.duplicated().sum()
    )

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

    # ---------------------------------------
    # AI Insights
    # ---------------------------------------

    insights = []

    if missing_values == 0:
        insights.append(
            "The dataset has no missing values."
        )
    else:
        insights.append(
            f"The dataset contains {missing_values} missing values."
        )

    if duplicates == 0:
        insights.append(
            "No duplicate records were found."
        )
    else:
        insights.append(
            f"The dataset contains {duplicates} duplicate records."
        )

    if numeric_columns > categorical_columns:
        insights.append(
            "The dataset is primarily numerical and suitable for statistical analysis and machine learning."
        )
    else:
        insights.append(
            "The dataset contains more categorical features and is suitable for business analysis."
        )

    insights.append(
        f"The dataset contains {rows} rows and {columns} columns."
    )

    # ---------------------------------------
    # Generate Chart
    # ---------------------------------------

    chart_file = None

    numeric_cols = df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_cols) > 0:

        column = numeric_cols[0]

        plt.figure(figsize=(8, 5))

        try:

            if df[column].nunique() <= 20:

                df[column].value_counts().plot(
                    kind="bar"
                )

                plt.title(
                    f"{column} Distribution"
                )

            else:

                sample = df[column].dropna().sample(
                    min(5000, len(df[column].dropna())),
                    random_state=42
                )

                sample.plot(
                    kind="hist",
                    bins=30
                )

                plt.title(
                    f"{column} Histogram"
                )

            plt.tight_layout()

            chart_file = f"{uuid.uuid4().hex}.png"

            chart_path = os.path.join(
                CHART_FOLDER,
                chart_file
            )

            plt.savefig(chart_path)

        finally:

            plt.close()

    # ---------------------------------------
    # Show Report
    # ---------------------------------------

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
    # --------------------------------------------------
# Download PDF Report
# --------------------------------------------------

@app.route("/download-report")
def download_report():

    pdf_file = "InsightForge_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(
        Paragraph(
            "InsightForge - Dataset Analysis Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    # Date
    current_date = datetime.now().strftime("%d %B %Y, %I:%M %p")

    story.append(
        Paragraph(
            f"<b>Generated on:</b> {current_date}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    # Information
    story.append(
        Paragraph(
            "Dataset Information",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "This report was generated automatically by InsightForge.",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 15))

    # AI Insights
    story.append(
        Paragraph(
            "AI Insights",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "• Dataset uploaded and analyzed successfully.",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "• Dataset statistics are available on the dashboard.",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "• Charts were automatically generated for numerical data.",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "• InsightForge provides quick AI-powered dataset analysis.",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    # Add latest chart
    try:

        chart_files = [
            f for f in os.listdir(CHART_FOLDER)
            if f.endswith(".png")
        ]

        if chart_files:

            chart_files.sort(
                key=lambda x: os.path.getmtime(
                    os.path.join(CHART_FOLDER, x)
                )
            )

            latest_chart = os.path.join(
                CHART_FOLDER,
                chart_files[-1]
            )

            story.append(
                Paragraph(
                    "Data Visualization",
                    styles["Heading2"]
                )
            )

            story.append(
                Image(
                    latest_chart,
                    width=450,
                    height=280
                )
            )

            story.append(Spacer(1, 20))

    except Exception:
        pass

    # Footer
    story.append(
        Paragraph(
            "Generated using InsightForge",
            styles["Italic"]
        )
    )

    story.append(
        Paragraph(
            "Developed by Kripa Patel",
            styles["Italic"]
        )
    )

    doc.build(story)

    return send_file(
        pdf_file,
        as_attachment=True
    )


# --------------------------------------------------
# Friendly Error Pages
# --------------------------------------------------

@app.errorhandler(413)
def file_too_large(error):

    return render_template(
        "error.html",
        message="File too large! Please upload a CSV smaller than 20 MB."
    ), 413


@app.errorhandler(500)
def internal_error(error):

    return render_template(
        "error.html",
        message="Something went wrong while processing your dataset. Please try another CSV."
    ), 500


# --------------------------------------------------
# Run Application
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)