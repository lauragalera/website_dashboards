import os
from flask import Flask, render_template
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from flask import request


app = Flask(__name__)

def get_dropdown_options():
    df = pd.read_csv('static/data/df_classrooms_product_week.csv')  # Replace with your CSV filename
    return df

@app.route('/')
def home():
    image_folder = os.path.join(app.static_folder, 'images')
    images = [img for img in os.listdir(image_folder) if img.startswith("formula")]
    return render_template('index.html', images=images, main_image="badger.png")

@app.route('/myclasses')
def myclasses():
    options = get_dropdown_options()
    return render_template('my_classes.html', options=options.to_dict('records'))

@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/dashboard_page', methods=['GET'])
def dashboard_page():
    classroom_id = request.args.get('classroom_id')

    print(classroom_id)
    # Add debug print to verify the valuew
    return render_template('main.html', classroom_id=classroom_id)

if __name__ == '__main__':
    app.run(debug=True)
