from application import create_app
from flask import redirect

app = create_app('ProductionConfig')


@app.route('/')
def index():
    return redirect('/api/docs')


if __name__ == '__main__':
    app.run()