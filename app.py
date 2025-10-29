import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# ------------------------------
# Load dataset
# ------------------------------
df = pd.read_csv('bank_transactions.csv')
df = df.dropna()

if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()

# ------------------------------
# Themes
# ------------------------------
LIGHT_THEME = {
    "background": "#f5f7fa",
    "card": "white",
    "text": "#333",
    "header": "#0b5394",
    "shadow": "0 4px 12px rgba(0,0,0,0.1)"
}

DARK_THEME = {
    "background": "#1e1e2f",
    "card": "#2b2b40",
    "text": "#e0e0e0",
    "header": "#1e88e5",
    "shadow": "0 4px 12px rgba(255,255,255,0.1)"
}

# ------------------------------
# App setup
# ------------------------------
app = Dash(__name__)
app.title = "🏦 Banking Dashboard"

years_available = sorted(df['Year'].dropna().unique().astype(int))

# ------------------------------
# Layout
# ------------------------------
app.layout = html.Div(
    id="main-div",
    style={
        "fontFamily": "Segoe UI, sans-serif",
        "padding": "30px",
        "transition": "background-color 0.5s ease, color 0.5s ease",
    },
    children=[
        html.Div(
            id="header-div",
            style={
                "textAlign": "center",
                "padding": "20px",
                "borderRadius": "10px",
                "marginBottom": "20px",
                "transition": "background-color 0.5s ease, color 0.5s ease",
            },
            children=[
                html.H1(
                    "🏦 Banking Customer Transaction Analysis",
                    style={"marginBottom": "10px"}
                ),
                html.P(
                    "Analyze and visualize customer transactions (2015–2025) interactively",
                    style={"fontSize": "18px"}
                ),
                html.Div(
                    style={"marginTop": "10px"},
                    children=[
                        html.Label("🌙 Dark Mode", style={"marginRight": "10px", "fontWeight": "bold"}),
                        dcc.RadioItems(
                            id="theme-toggle",
                            options=[
                                {"label": "Off", "value": "light"},
                                {"label": "On", "value": "dark"},
                            ],
                            value="light",
                            inline=True,
                            inputStyle={"marginRight": "5px", "marginLeft": "10px"},
                            style={"display": "inline-block"}
                        ),
                    ],
                ),
            ],
        ),

        html.Div(
            id="content-card",
            style={
                "borderRadius": "12px",
                "padding": "25px",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.1)",
                "maxWidth": "950px",
                "margin": "auto",
                "transition": "background-color 0.5s ease, color 0.5s ease",
            },
            children=[
                html.Div(
                    style={
                        "display": "flex",
                        "gap": "20px",
                        "justifyContent": "space-between",
                        "marginBottom": "20px",
                    },
                    children=[
                        html.Div(
                            style={"flex": "1"},
                            children=[
                                html.Label(
                                    "Select Visualization Type:",
                                    style={
                                        "fontWeight": "bold",
                                        "fontSize": "16px",
                                        "display": "block",
                                        "marginBottom": "5px",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="plot-dropdown",
                                    options=[
                                        {"label": "Count by Transaction Type", "value": "count_type"},
                                        {"label": "Amount Distribution by Transaction Type", "value": "amount_type"},
                                        {"label": "Monthly Transaction Amount Sum", "value": "monthly_sum"},
                                    ],
                                    value="count_type",
                                    clearable=False,
                                    style={"borderRadius": "8px"},
                                ),
                            ],
                        ),
                        html.Div(
                            style={"flex": "1"},
                            children=[
                                html.Label(
                                    "Select Year:",
                                    style={
                                        "fontWeight": "bold",
                                        "fontSize": "16px",
                                        "display": "block",
                                        "marginBottom": "5px",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="year-dropdown",
                                    options=[{"label": str(y), "value": y} for y in years_available],
                                    value=None,
                                    placeholder="All Years",
                                    clearable=True,
                                    style={"borderRadius": "8px"},
                                ),
                            ],
                        ),
                    ],
                ),
                dcc.Graph(id="graph-output", style={"height": "600px"}),
            ],
        ),
    ],
)

# ------------------------------
# Callbacks
# ------------------------------
@app.callback(
    Output("graph-output", "figure"),
    Output("main-div", "style"),
    Output("header-div", "style"),
    Output("content-card", "style"),
    Input("plot-dropdown", "value"),
    Input("year-dropdown", "value"),
    Input("theme-toggle", "value"),
)
def update_graph(selected_option, selected_year, theme_choice):
    theme = DARK_THEME if theme_choice == "dark" else LIGHT_THEME
    dff = df.copy()

    if selected_year:
        dff = dff[dff["Year"] == selected_year]

    # -------------------- Graphs --------------------
    if selected_option == "count_type":
        fig = px.histogram(
            dff,
            x="Transaction_Type",
            color="Transaction_Type",
            title=f"Count of Transactions by Type{' - ' + str(selected_year) if selected_year else ''}",
            template="plotly_dark" if theme_choice == "dark" else "simple_white",
        )

    elif selected_option == "amount_type":
        fig = px.box(
            dff,
            x="Transaction_Type",
            y="Amount",
            color="Transaction_Type",
            title=f"Transaction Amount by Type{' - ' + str(selected_year) if selected_year else ''}",
            template="plotly_dark" if theme_choice == "dark" else "simple_white",
        )

    elif selected_option == "monthly_sum":
        if "Month" not in dff.columns:
            return px.scatter(title="No Month data available"), {}, {}, {}
        monthly = dff.groupby("Month", sort=False)["Amount"].sum().reset_index()
        fig = px.line(
            monthly,
            x="Month",
            y="Amount",
            markers=True,
            title=f"Monthly Transaction Amount Sum{' - ' + str(selected_year) if selected_year else ''}",
            template="plotly_dark" if theme_choice == "dark" else "simple_white",
        )

    else:
        fig = px.histogram(
            dff,
            x="Transaction_Type",
            title="Count of Transactions by Type",
            template="plotly_dark" if theme_choice == "dark" else "simple_white",
        )

    # -------------------- Figure Styling --------------------
    fig.update_layout(
        title_font_size=22,
        title_x=0.5,
        plot_bgcolor=theme["background"],
        paper_bgcolor=theme["background"],
        font=dict(family="Segoe UI", size=14, color=theme["text"]),
        margin=dict(l=40, r=40, t=80, b=40),
        transition_duration=500,
    )

    # -------------------- Theming --------------------
    main_style = {
        "fontFamily": "Segoe UI, sans-serif",
        "backgroundColor": theme["background"],
        "padding": "30px",
        "color": theme["text"],
        "transition": "background-color 0.5s ease, color 0.5s ease",
    }
    header_style = {
        "textAlign": "center",
        "backgroundColor": theme["header"],
        "padding": "20px",
        "borderRadius": "10px",
        "color": "white",
        "boxShadow": theme["shadow"],
        "transition": "background-color 0.5s ease, color 0.5s ease",
    }
    card_style = {
        "backgroundColor": theme["card"],
        "borderRadius": "12px",
        "padding": "25px",
        "boxShadow": theme["shadow"],
        "maxWidth": "950px",
        "margin": "auto",
        "color": theme["text"],
        "transition": "background-color 0.5s ease, color 0.5s ease",
    }

    return fig, main_style, header_style, card_style


# ------------------------------
# Run app
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
