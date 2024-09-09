from flask import Flask , render_template


def create_app():
    app = Flask(__name__)

app = create_app()


@app.route('/')
def home() :
    render_template('index.html')



def detectEmotion(image_path):
    with open(image_path,'rb') as image_stream:
        detected_faces = face_client.face.detect_with_stream(image = image_stream ,
                                                             return_face_attributes =['emotion'])
        if not detected_faces:
            return "No face detected"


        emotions=detected_faces[0].face_attributes.emotion
        emotion_scores = {
            'anger' : emotions.anger,
            'fear' : emotions.fear,
            'disgust' : emotions.disgust,
            'contempt' : emotions.contempt,
            'happiness' : emotions.happiness,
            'neutral' : emotions.neutral,
            'sadness' : emotions.sadness,
            'surprise' : emotions.surprise,
        }
        return emotion_scores

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