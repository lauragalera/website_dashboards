from flask import Flask, render_template
import os

app = Flask(__name__)

def get_orbit_images():
    """Auto-discover orbit images with error handling"""
    try:
        return [f for f in os.listdir('static/images') 
                if f.startswith('orbit') and f.endswith(('.png', '.jpg'))]  # Fixed typo: 'orbits' → 'orbit'
    except FileNotFoundError:
        return [] 

@app.route('/')
def home():
    return render_template('index.html', 
        main_image='badger.png',
        orbit_images=get_orbit_images()
    )

# Add this to run the server
if __name__ == '__main__':
    app.run(debug=True)  # Starts the server on port 5000