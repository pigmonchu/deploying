from app import app

@app.route('/')
def index():
    return 'Lo que queramos'