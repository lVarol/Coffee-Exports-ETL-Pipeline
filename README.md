
# Coffee Exports ETL Pipeline & Visualization App ☕ co

This project is a complete ETL (Extract, Transform, Load) pipeline combined with a Flask web application for visualizing Colombian coffee exports.
It extracts data from an Excel file, transforms and cleans the data, loads it into a database, and then displays interactive visualizations via a Flask application.
ETL python code applies OOP concepts.

Original Data Source: https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Ffederaciondecafeteros.org%2Fapp%2Fuploads%2F2024%2F04%2FExportaciones.xlsx&wdOrigin=BROWSELINK

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)


## Features

- **ETL Pipeline:**  
  - Extracts data from an Excel file (`Exportations.xlsx`).
  - Transforms and cleans the data using Pandas.
  - Loads the cleaned data into a SQL database.
  
- **Flask Visualization App:**  
  - Displays interactive graphs (generated with Plotly) showing coffee export trends.
  - Provides updated visualizations based on ETL data.
  
- **Automated Scheduling:**  
  - Uses cron to run the ETL pipeline every two weeks (Original source is updated once a month).
  
- **Production Deployment:**
  - Deployed in AWS ec2 instance.   
  - Served with Gunicorn as a WSGI server.
  - Managed by systemd for automatic start/restart.
  - Nginx is used as a reverse proxy to route incoming HTTP requests to the Flask app.

## Technologies Used

- **Python 3.9+**: Main programming language.
- **Flask**: Web framework for the visualization app.
- **Pandas**: Data manipulation and ETL.
- **Plotly**: Interactive graph generation.
- **SQLAlchemy / sqlite3**: Database connectivity (or another SQL backend).
- **Gunicorn**: Production-grade WSGI server.
- **systemd**: Process management (service file for Gunicorn).
- **Nginx**: Reverse proxy server.
- **Cron**: Scheduling ETL jobs.
- **Celery (Optional)**: For asynchronous task processing (if used).

## Project Structure

```plaintext
Coffee-Exports-ETL-Pipeline/
├── etl/
│   ├── etl_pipeline.py         # Main ETL pipeline script
│   ├── extract.py              # Module for extracting data from Excel
│   ├── transform.py            # Module for transforming data
│   └── load.py                 # Module for loading data into the database
├── visualizations/
│   ├── app.py                  # Flask application code
│   ├── wsgi.py                 # WSGI entry point for Gunicorn
│   ├── templates/
│   │   └── index.html          # HTML template(s) for the Flask app
│   └── static/                 # Static assets (CSS, JS, images, etc.)
├── cron.log                    # Log file for cron job outputs
├── cron_script (Optional)      # Script file for a custom cron wrapper (if needed)
├── README.md                   # This file
└── venv/                       # Virtual environment with project dependencies

1. Copy the content above into a file named `README.md` in your project root.
2. Customize any paths, dates, or details specific to your project.
3. Commit the README to your repository:
   ```bash
   git add README.md
   git commit -m "Add project README"
   git push origin main


Preliminary figures corresponding to the provisional declared value in the export declaration.
The FNC publishes these figures for illustrative purposes and they should not be considered an official source for the value of coffee exports.
 The official source is the consolidated and definitive figures regularly published by the DIAN.
