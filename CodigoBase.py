import cv2
import argparse
import numpy as np
from pygame import mixer

#Song load and volume settings
mixer.init()
mixer.music.load("Quieres_Ser_Mi_Novia.mp3")
mixer.music.set_volume(0.7)

def transparenteOverlay(src, overlay , pos = (0,0)  , scale = 1):
    overlay = cv2.resize(overlay , (0,0) ,fx = scale , fy = scale)
    h, w, _ =  overlay.shape # tamaño de la imagen de primer plano
    rows, cols , _ = src.shape  # tamaño de la imagen de fondo
    y, x = pos[0] , pos [1]

    for i in range(h):
        for j in range(w):
            if x + i > rows or y + j >=cols:
                continue
            alpha = float(overlay[i][j][3]/255) # leer el canal alfa
            src[x+i][y+j] = alpha * overlay[i][j][:3] + (1-alpha) * src[x+i][y+j]
    return src

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Camera visualization')

    ### Positional arguments
    parser.add_argument('-i', '--cameraSource', default=0, help="Introduce number or camera path, default is 0 (default cam)")

    
    args = vars(parser.parse_args())


    cap = cv2.VideoCapture(args["cameraSource"]) #0 local o primary camera

    cascada = cv2.CascadeClassifier('face.xml') # método eficaz para la detección de objetos (cara)
    lentes_var = cv2.imread("lentes.png" , -1) # leer la imagen de los lentes que se van a mostrar 
    #The song plays
    mixer.music.play()
    
    while cap.isOpened():
        
        #BGR image feed from camera

        success,img = cap.read()    
        if success:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
            #convertimos la imagen a una matriz RGB
            img = np.array(img, dtype=np.float64)
            img = cv2.transform(img, np.matrix([[0.400, 0.130, 0.200],[0.100, 0.200, 0.130],[0.140, 0.180, 0.180]])) #seleccionamos los valores RGB para dar una tonalidad rojiza a la imagen
            img[np.where(img > 255)] = 255 # cualquier valor mayor a 255, igualarlo a 255
            img = np.array(img, dtype=np.uint8)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
            gris = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # convirtiendo de color a grises
            faces =cascada.detectMultiScale(gris ,1.3 , 5 , 0 , minSize=(120,120) , maxSize=(350,350)) 
            # para detectar objetos de diferentes tamaños

            for (x,y,w,h) in faces:
                if h> 0 and w>0:
                    # tamaños para los lentes
                    lentes_symin = int(y+ 1.5 * h/5)
                    lentes_symax = int(y + 2.5 * h /5)
                    sh_glass = lentes_symax - lentes_symin

                    lentes_ori = img [lentes_symin:lentes_symax, x:x+w]
                    lentes_mostrar = cv2.resize(lentes_var, (w, sh_glass), interpolation= cv2.INTER_CUBIC)
                    transparenteOverlay(lentes_ori, lentes_mostrar)


        if not success:
            break
        if img is None:
            break

        
        cv2.imshow("Video webcam", img)

        k = cv2.waitKey(10)
        if k==27:
            #The song stops
            mixer.music.stop()
            break


    cap.release()
    cv2.destroyAllWindows()

# Basado de: https://www.youtube.com/watch?v=xn9egHOQ16k
