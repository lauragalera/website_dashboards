import os
from flask import Flask, render_template
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from plotly_plots import teacher_plots

app = Flask(__name__)

@app.route('/')
def home():
    image_folder = os.path.join(app.static_folder, 'images')
    images = [img for img in os.listdir(image_folder) if img.startswith("formula")]
    return render_template('index.html', images=images, main_image="badger.png")

# Create Dash app
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')


# Layout
dash_app.layout = html.Div(children=[
    html.H1("Teacher Dashboard"),
    dcc.Graph(figure=teacher_plots.bubble_chart_plot())
])

# Flask Route
@app.route('/dashboard')
def dashboard():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
