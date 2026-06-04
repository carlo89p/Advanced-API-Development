from application import create_app

app = create_app('ProductionConfig')

if __name__ == '__main__':
    app.run()from application import create_app
from flask import redirect

app = create_app('ProductionConfig')

@app.route('/')
def index():
    return redirect('/api/docs')

if __name__ == '__main__':
    app.run()