
# il codice per gestire gli input dev'essere qui
from flask import Flask, request, Response
import cv2 as cv
import oda as od
import json
app = Flask(__name__)


@app.route('/')
def index():
    return 'Tesina Computer Vision'


@app.route('/image', methods=['POST', 'GET'])
def image():
    try:
        print("prima di richiedere l'immGINE");
        image_file = request.files['image']  # get the image

        ''' chiami il metodo che 
        elabora l'immagine e manfa il Json con la posizione del tavolo'''
        #image = cv.imread(image_file);
        #cv.imshow("img",image);
        #cv.imwrite("result.jpg", image);
        print("sono qui");
        # return image_file;
        return json.dumps("worked");
    except Exception as e:

        print('POST /image error: ' + str(e))
        return e;

@app.route('/local', methods=['GET', 'POST'])
def local():
    return Response(open('./static/local.html').read(), mimetype="text/html")


@app.route('/video')
def remote():
    return Response(open('./static/video.html').read(), mimetype="text/html")


# for CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')  # Put any other methods you need here
    return response

if __name__ == '__main__':
    app.run();