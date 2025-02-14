import os
from flask import Flask, render_template, send_file
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from prophet import Prophet
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest

app = Flask(__name__)

CLEANED_DATA_PATH = os.path.abspath(os.path.join("..", "data", "Exportations_cleaned.xlsx"))
DATABASE_PATH = os.path.abspath(os.path.join("..", "database", "exportations.db"))
TABLE_NAME = "colombian_coffee_exports"

# Create the engine with NO context manager usage
engine = create_engine(f"sqlite:///{DATABASE_PATH}")


@app.route("/download")
def download_file():
    # Just return the file
    return send_file(CLEANED_DATA_PATH, as_attachment=True)


def fetch_last_update():
    query = """
        SELECT 
            CAST(Year AS TEXT) || '-' || CAST(Month AS TEXT) AS Last_Update
        FROM colombian_coffee_exports
        ORDER BY Year DESC, Month DESC
        LIMIT 1;
    """
    # Manually open/close raw DB-API connection
    conn = engine.raw_connection()
    try:
        df = pd.read_sql(query, conn)
    finally:
        conn.close()
    return df.iloc[0, 0]


def fetch_data_g1():
    query = """
        SELECT Year, SUM(`Bags of 60 Kg. Exported`) AS Total_Exports
        FROM colombian_coffee_exports
        GROUP BY Year
        ORDER BY Year;
    """
    conn = engine.raw_connection()
    try:
        df = pd.read_sql(query, conn)
    finally:
        conn.close()
    return df


def fetch_data_g2():
    query = """
        SELECT Type_of_Coffee, COUNT(`Bags of 60 Kg. Exported`) AS Count_Exports
        FROM colombian_coffee_exports
        GROUP BY Type_of_Coffee
        ORDER BY Type_of_Coffee;
    """
    conn = engine.raw_connection()
    try:
        df = pd.read_sql(query, conn)
    finally:
        conn.close()
    return df


def fetch_data_g3():
    query = """
        SELECT Destination_Country, SUM(`Bags of 60 Kg. Exported`) AS Total_Exports
        FROM colombian_coffee_exports
        GROUP BY Destination_Country
        ORDER BY Total_Exports DESC
        LIMIT 10;
    """
    conn = engine.raw_connection()
    try:
        df = pd.read_sql(query, conn)
    finally:
        conn.close()
    return df


def fetch_data_g4():
    query = """
        SELECT 
            CAST(Year AS TEXT) || '-' || CAST(Month AS TEXT) AS Año_unico,
            SUM(`Bags of 60 Kg. Exported`) AS Total_Exports
        FROM colombian_coffee_exports
        GROUP BY Year, Month
        ORDER BY Year ASC, Month ASC;
    """
    conn = engine.raw_connection()
    try:
        df = pd.read_sql(query, conn)
    finally:
        conn.close()
    return df


@app.route("/")
def index():
    last_update = fetch_last_update()

    # --- Graph 1 ---
    d1 = fetch_data_g1()
    fig1 = px.bar(
        d1, x="Year", y="Total_Exports", text_auto=".3s",
        title="Colombian Coffee Exports Over Time",
        labels={"Year": "Year", "Total_Exports": "Bags of 60Kg Exported"}
    )
    fig1.update_layout(
        title={'x': 0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': dict(weight='bold')},
        paper_bgcolor="#F7F7F7",
        yaxis_title='Bags of 60 Kg',
        xaxis_title='Year',
        font=dict(size=14),
        yaxis=dict(showgrid=True, gridcolor='lightgray', range=[1e6, 15e6]),
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
    )

    # --- Graph 2 ---
    d2 = fetch_data_g2()
    fig2 = px.pie(
        d2, values="Count_Exports", names="Type_of_Coffee",
        title="Type of Coffee",
        labels={'Total_Exports': 'Exports'}
    )
    fig2.update_layout(
        title={'x': 0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': dict(weight='bold')}
    )

    # --- Graph 3 ---
    d3 = fetch_data_g3()
    fig3 = px.bar(
        d3, x="Destination_Country", y="Total_Exports", text_auto=".3s",
        title="Top Countries that Export the Most<br>(2017–2025)",
        labels={
            "Destination_Country": "Destination Country",
            "Total_Exports": "Bags of 60Kg Exported"
        }
    )
    fig3.update_layout(
        title={'x': 0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': dict(weight='bold')},
        paper_bgcolor="#F7F7F7",
        yaxis_title='Bags of 60 Kg',
        xaxis_title='Destination Country',
        font=dict(size=14),
        yaxis=dict(showgrid=True, gridcolor='lightgray', range=[1e6, 45e6]),
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
    )

    # --- Graph 4 ---
    d4 = fetch_data_g4()
    fig4 = px.line(d4, x='Año_unico', y='Total_Exports', title="Trends Over Time")
    fig4.update_layout(
        title={'x': 0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': dict(weight='bold')},
        dragmode=False,
        plot_bgcolor='white',
        yaxis_title='Bags of 60 Kg',
        xaxis_title='Year',
        font=dict(size=14),
        yaxis=dict(showgrid=True, gridcolor='lightgray', range=[1e5, 1.8e6]),
        xaxis=dict(title_font=dict(weight='bold')),
        bargap=0.4,
        autosize=True,
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
    )

    # --- Prophet Forecast ---
    def create_prophet_plot():
        df = fetch_data_g4()
        df.rename(columns={'Año_unico': 'ds', 'Total_Exports': 'y'}, inplace=True)

        model = Prophet()
        model.fit(df)

        future = model.make_future_dataframe(periods=6, freq='M')
        forecast = model.predict(future)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['ds'], y=df['y'], mode='lines',
            name='Actual Exports', line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=forecast['ds'], y=forecast['yhat'], mode='lines',
            name='Forecast', line=dict(color='green', dash='dash')
        ))

        fig.update_layout(
            title=dict(
                text="Coffee Export Forecast",
                x=0.5,
                xanchor='center',
                yanchor='top',
                font=dict(weight='bold')
            ),
            xaxis_title="Date",
            yaxis_title="Bags of 60Kg Exported",
            xaxis=dict(tickangle=-45),
            dragmode=False,
            bargap=0.4,
            autosize=True,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.4,
                xanchor="center",
                x=0.5
            )
        )
        return fig

    # --- Anomaly Detection ---
    def detect_anomalies():
        df = fetch_data_g4()

        iso_forest = IsolationForest(contamination=0.05, random_state=42)
        df['Anomaly'] = iso_forest.fit_predict(df[['Total_Exports']])
        df['Anomaly_Label'] = df['Anomaly'].map({1: "Normal", -1: "Anomaly"})

        fig = px.scatter(
            df, x="Año_unico", y="Total_Exports", color="Anomaly_Label",
            title="Anomaly Detection in Coffee Exports",
            labels={"Año_unico": "Year-Month", "Total_Exports": "Bags of 60Kg Exported"},
            color_discrete_map={"Normal": "blue", "Anomaly": "red"}
        )
        fig.update_layout(
            title=dict(
                text="Anomaly Detection in Coffee Exports",
                x=0.5,
                xanchor='center',
                yanchor='top',
                font=dict(weight='bold')
            ),
            margin=dict(l=20, r=20, t=30, b=20),
            bargap=0.4,
            autosize=True,
            dragmode=False,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.4,
                xanchor="center",
                x=0.5
            )
        )
        return fig

    figml = create_prophet_plot()
    figml2 = detect_anomalies()

    return render_template(
        "index.html",
        last_update=last_update,
        graph_html1=fig1.to_html(full_html=False, config={"staticPlot": True}),
        graph_html2=fig2.to_html(full_html=False, config={"staticPlot": False}),
        graph_html3=fig3.to_html(full_html=False, config={"staticPlot": True}),
        graph_html4=fig4.to_html(full_html=False, config={"staticPlot": False}),
        graph_html5=figml.to_html(full_html=False, config={"staticPlot": False}),
        graph_html6=figml2.to_html(full_html=False, config={"staticPlot": False})
    )


if __name__ == "__main__":
    app.run(debug=True)
