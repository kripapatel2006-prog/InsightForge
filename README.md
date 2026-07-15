# InsightForge

InsightForge is an AI-powered data analytics web application built using Flask and Python. It enables users to upload CSV datasets, perform instant data analysis, visualize key statistics, and receive automated insights through an interactive and user-friendly dashboard.

---

## Features

- Upload CSV datasets
- Dataset summary (Rows, Columns, Missing Values, Duplicate Rows)
- Dataset preview
- File information
- Memory usage analysis
- Numeric and categorical column detection
- AI-generated dataset insights
- Automatic data visualization
- Professional dashboard interface

---

## Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Libraries
- Pandas
- Matplotlib
- NumPy

---

## Project Structure

```
InsightForge/
│
├── app.py
├── requirements.txt
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── charts/
│
├── templates/
│   ├── index.html
│   ├── upload.html
│   └── report.html
│
├── uploads/
│
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/InsightForge.git
```

Navigate into the project

```bash
cd InsightForge
```

Install the required packages

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser and visit

```
http://127.0.0.1:5000
```

---

## How It Works

1. Upload a CSV dataset.
2. The application reads the dataset using Pandas.
3. InsightForge analyzes:
   - Total rows
   - Total columns
   - Missing values
   - Duplicate rows
   - Memory usage
   - Numeric and categorical columns
4. AI-generated insights are displayed.
5. A data visualization chart is generated automatically.
6. The dataset preview is presented in a professional report layout.

---

## Future Enhancements

- Interactive Plotly visualizations
- Correlation heatmap
- Histogram and scatter plots
- Excel (.xlsx) file support
- Data cleaning tools
- Machine Learning model training
- Downloadable PDF reports
- User authentication
- Dark mode
- Cloud deployment

---

## Screenshots

### Home Page

_Add screenshot here_

### Upload Dataset

_Add screenshot here_

### Analysis Report

_Add screenshot here_

---

## Author

**Kripa Patel**

Computer Science Engineering (Data Science)

Vignana Bharathi Institute of Technology

---

## License

This project is developed for educational and portfolio purposes.