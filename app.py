import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# ------------------------------
# Load dataset
# ------------------------------
df = pd.read_csv("bank_transactions.csv")
df = df.dropna()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month_name()
df["Month_Num"] = df["Date"].dt.month

month_order = (
    df[["Month", "Month_Num"]]
    .drop_duplicates()
    .sort_values("Month_Num")["Month"]
    .tolist()
)

# ------------------------------
# App Setup
# ------------------------------
app = Dash(__name__)
app.title = "Banking Transaction Analytics"

years = sorted(df["Year"].dropna().unique().astype(int))

# ------------------------------
# KPI CALCULATIONS
# ------------------------------
def kpi_values(data):
    total = data["Amount"].sum()
    credit = data[data["Transaction_Type"] == "Credit"]["Amount"].sum()
    debit = data[data["Transaction_Type"] == "Debit"]["Amount"].sum()
    net = credit - debit
    return total, credit, debit, net

# ------------------------------
# Layout
# ------------------------------
app.layout = html.Div(
    style={
        "backgroundColor": "#f5f7fa",
        "color": "#222",
        "fontFamily": "Segoe UI",
        "padding": "30px",
    },
    children=[
        html.H1(
            "🏦 Banking Transaction Analytics Dashboard",
            style={"textAlign": "center"},
        ),
        html.P(
            "Exploratory Data Analysis & Visualization (2015–2025)",
            style={"textAlign": "center", "color": "#555"},
        ),

        # ---------------- KPI CARDS ----------------
        html.Div(
            id="kpi-cards",
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(4, 1fr)",
                "gap": "20px",
                "marginTop": "30px",
            },
        ),

        # ---------------- Controls ----------------
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr 1fr",
                "gap": "20px",
                "marginTop": "30px",
            },
            children=[
                dcc.Dropdown(
                    id="year-filter",
                    options=[{"label": "All Years", "value": "ALL"}]
                    + [{"label": str(y), "value": y} for y in years],
                    value="ALL",
                ),
                dcc.Dropdown(
                    id="chart-filter",
                    options=[
                        {"label": "Credit vs Debit Distribution", "value": "donut"},
                        {"label": "Monthly Transaction Trend", "value": "trend"},
                        {"label": "Transaction Amount Distribution", "value": "box"},
                        {"label": "Transaction Heatmap", "value": "heatmap"},
                    ],
                    value="donut",
                ),
                dcc.RadioItems(
                    id="animation-toggle",
                    options=[
                        {"label": "Animation OFF", "value": "off"},
                        {"label": "Animation ON", "value": "on"},
                    ],
                    value="off",
                    inline=True,
                ),
            ],
        ),

        # ---------------- Graph ----------------
        dcc.Graph(
            id="main-graph",
            style={"marginTop": "30px", "height": "550px"},
        ),
    ],
)

# ------------------------------
# Callback
# ------------------------------
@app.callback(
    Output("kpi-cards", "children"),
    Output("main-graph", "figure"),
    Input("year-filter", "value"),
    Input("chart-filter", "value"),
    Input("animation-toggle", "value"),
)
def update_dashboard(selected_year, chart_type, animation_mode):
    data = df.copy()
    if selected_year != "ALL":
        data = data[data["Year"] == selected_year]

    total, credit, debit, net = kpi_values(data)

    cards = [
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "12px",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.1)",
                "textAlign": "center",
            },
            children=[html.H4(label), html.H2(value)],
        )
        for label, value in [
            ("Total Amount", f"₹ {total:,.0f}"),
            ("Total Credit", f"₹ {credit:,.0f}"),
            ("Total Debit", f"₹ {debit:,.0f}"),
            ("Net Balance", f"₹ {net:,.0f}"),
        ]
    ]

    transition_time = 600 if animation_mode == "on" else 0

    if chart_type == "donut":
        fig = px.pie(
            data,
            names="Transaction_Type",
            values="Amount",
            hole=0.5,
            title="Credit vs Debit Distribution",
        )

    elif chart_type == "trend":
        monthly = (
            data.groupby(["Month", "Month_Num"])["Amount"]
            .sum()
            .reset_index()
            .sort_values("Month_Num")
        )
        fig = px.line(
            monthly,
            x="Month",
            y="Amount",
            markers=True,
            category_orders={"Month": month_order},
            title="Monthly Transaction Trend",
        )

    elif chart_type == "box":
        fig = px.box(
            data,
            x="Transaction_Type",
            y="Amount",
            color="Transaction_Type",
            title="Transaction Amount Distribution & Outliers",
        )

    else:
        heat = (
            data.groupby(["Month", "Transaction_Type"])["Amount"]
            .sum()
            .reset_index()
        )
        fig = px.density_heatmap(
            heat,
            x="Month",
            y="Transaction_Type",
            z="Amount",
            category_orders={"Month": month_order},
            title="Transaction Heatmap (Month vs Type)",
        )

    fig.update_layout(
        template="simple_white",
        title_x=0.5,
        transition_duration=transition_time,
    )

    return cards, fig

# ------------------------------
# Run App
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
