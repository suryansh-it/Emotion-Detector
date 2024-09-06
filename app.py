from flask import Flask , render_template


def create_app():
    app = Flask(__name__)

app = create_app()


@app.route('/')
def home() :
    render_template('index.html')





if __name__ == '__main__':
    app.run(debug=True)