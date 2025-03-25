import os
from flask import Flask, render_template
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


app = Flask(__name__)

@app.route('/')
def home():
    image_folder = os.path.join(app.static_folder, 'images')
    images = [img for img in os.listdir(image_folder) if img.startswith("formula")]
    return render_template('index.html', images=images, main_image="badger.png")

# Create Dash app
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')

# Sample Data
df = px.data.gapminder().query("year == 2007").head(10)

# Bar Chart
fig = px.bar(df, x='country', y='gdpPercap', title="GDP Per Capita by Country")

# Layout
dash_app.layout = html.Div(children=[
    html.H1("Simple Dashboard"),
    dcc.Graph(figure=fig)
])

# Flask Route
@app.route('/dashboard')
def dashboard():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
