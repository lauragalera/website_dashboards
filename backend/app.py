import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    image_folder = os.path.join(app.static_folder, 'images')
    images = [img for img in os.listdir(image_folder) if img.startswith("formula")]
    return render_template('index.html', images=images, main_image="badger.png")

@app.route('/dashboard_main')
def 


if __name__ == '__main__':
    app.run(debug=True)
