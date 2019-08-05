import cv2
import matplotlib.pyplot as plt
import numpy as np


def handle_close( event, cap):
     cap.release()

def main():
    # indica la webcam
    cap = cv2.VideoCapture(0)
    t = 100 # treshold for canny detection edge
    w = 640.0 #width we want
    #abilita modo interattivo, va copiato su
    plt.ion()
    fig = plt.figure()
    #a questa figura ci agganciamo
    fig.canvas.mpl_connect("close event", lambda event: handle_close(event)) #quando chiudiamo la finestra si chiuderà anche il video!
    #inizializzazione
    image = None
    while cap.isOpened():
        # ret viene usato in caso di errore
        ret, image = cap.read()
        width, height, depth = image.shape
        scale = w / width
        h = height * scale;

        image = cv2.resize(image, (0, 0), fx=scale, fy=scale)

        # Apply filters
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blured = cv2.medianBlur(grey, 15)

        # Compose 2x2 grid with all previews
        grid = np.zeros([h*2, w*2, 3], np.uint8)
        grid[0:h, 0:w] = image

        # We need to convert each of them to RGB from grescaled 8 bit format
        """rispetto al codice trovato online ho dovuto invertire width con height"""
        grid[h:2 * h, 0:w] = np.dstack([cv2.Canny(grey, t / 2, t)] * 3)
        grid[0:h, w:2 * w] = np.dstack([blured] * 3)
        grid[h:2 * h, w:2 * w] = np.dstack([cv2.Canny(blured, t / 2, t)] * 3)
        """ sarebbe meglio cambiare la dimensione, ma come faccio?"""
        cv2.imshow('Image previews', grid)

        if image is None:
            #convertire il fram in RGB xké è in BGR
            image = plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            plt.axis("off")
            plt.title('Camera stream')
        else:
            image.set_data(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))#rimpiazza il contenuto di imgshow senza rimpiazzare gli assi il titolo ...
            fig.canvas.draw() # disegna il nuovo dato
            plt.pause(1/30)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)