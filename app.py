from flask import Flask , render_template


def create_app():
    app = Flask(__name__)

app = create_app()


@app.route('/')
def home() :
    render_template('index.html')

@app.route('/home', method= ['GET', 'POST'])
def capture():


@app.route('/home', method= ['GET', 'POST'])
def preview():


@app.route('/home' , method = ['GET'])
def emotion():


@app.route('home/login', method = ['GET' , 'POST'])
def login():

@app.route('home/Signup', method = ['GET' , 'POST'])
def signup():

@app.route('home/history' , method = ['GET'])
def history(): 

if __name__ == '__main__':
    app.run(debug=True)