from flask import Flask, render_template


from datetime import datetime, timedelta
import random
from database import init_db

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def initialize_app():
    init_db()
    


@app.route('/')
def home():
    return render_template('index.html')


# Generar datos de uso para los últimos 365 días
start_date = datetime.now() - timedelta(days=365)
usage_data = {
    (start_date + timedelta(days=i)).strftime('%Y-%m-%d'): random.randint(0, 10)
    for i in range(365)
}

@app.route('/profile')
def profile():
    # Pasar los datos de uso a la plantilla
    return render_template('profile.html', usage_data=usage_data)





initialize_app()