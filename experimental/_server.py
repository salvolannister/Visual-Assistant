
# il codice per gestire gli input dev'essere qui
from assistant.askassistant import ask, welcomeFrase
from flask import Flask, request, Response
import cv2 as cv
import object_detection_api as oda
from PIL import Image
import numpy as np
import webbrowser

choice = 0;

def switch(x):
    return {
        'identity': 0,
        'vase': 2,
        'painting': 1,

    }[x]




app = Flask(__name__)

# 0 doraemon
# 1 painting
# 2 vase



@app.route('/')
def index():
    return 'go to /local to start'


@app.route('/image', methods=['POST', 'GET'])
def image():
    try:
        print("prima di richiedere l'img");
        print(choice)
        image_file = request.files['image']  # get the image

        ''' chiami il metodo che 
        elabora l'immagine e manfa il Json con la posizione del tavolo'''
        #image = cv.imread(image_file);
        #cv.imshow("img",image);

        pil_image = Image.open(image_file)
        opencvImage = cv.cvtColor(np.array(pil_image), cv.COLOR_RGB2BGR)
        #cv.imwrite("result.jpg", opencvImage);
        # return image_file;
        return oda.getObjects(opencvImage, choice)
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
     #welcomeFrase()
    """
    print('How can i help you \n'
          '#0: to show my identity \n'
          '#1: to show a paint on the wall \n'
          '#2 to show a vase on your table\n'
          'input: ')
    """
    choise = ask();
    while choise == "-1":
        choise = ask()
    
    choice= switch(choise)


    webbrowser.open('http://127.0.0.1:5000/local')
    app.run();

