import cv2
import matplotlib.pyplot as plt
import numpy as np


def handle_close( event, cap):
     cap.release()

def main():
    # indica la webcam
    cap = cv2.VideoCapture(0)
    t = 100 # treshold for canny detection edge
    w = 640 #width we want
    #abilita modo interattivo, va copiato su
    plt.ion()
    fig = plt.figure()
    #a questa figura ci agganciamo
    fig.canvas.mpl_connect("close event", lambda event: handle_close(event)) #quando chiudiamo la finestra si chiuderà anche il video!
    #inizializzazione
    img = None
    while cap.isOpened():
        # ret viene usato in caso di errore
        ret, frame = cap.read()
        width, height, depth = frame.shape
        scale = w/ width
        h = height

        frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

        # Apply filters
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blured = cv2.medianBlur(grey, 15)

        # Compose 2x2 grid with all previews
        grid = np.zeros([w*2, h*2, 3], np.uint8)
        grid[0:w, 0:h] = frame

        # We need to convert each of them to RGB from grescaled 8 bit format
        """rispetto al codice trovato online ho dovuto invertire width con height"""
        grid[w:2 * w, 0:h] = np.dstack([cv2.Canny(grey, t / 2, t)] * 3)
        grid[0:w, h:2 * h] = np.dstack([blured] * 3)
        grid[w:2 * w, h:2 * h] = np.dstack([cv2.Canny(blured, t / 2, t)] * 3)
        """ sarebbe meglio cambiare la dimensione, ma come faccio?"""
        cv2.imshow('Image previews', grid)

        if img is None:
            #convertire il fram in RGB xké è in BGR
            img = plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            plt.axis("off")
            plt.title('Camera stream')
        else:
            img.set_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))#rimpiazza il contenuto di imgshow senza rimpiazzare gli assi il titolo ...
            fig.canvas.draw() # disegna il nuovo dato
            plt.pause(1/30)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)