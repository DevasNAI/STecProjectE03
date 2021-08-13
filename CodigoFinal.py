import cv2
import argparse
import numpy as np
from pygame import mixer

#############################################################
#
#   Código creado por:
#       Andrés Sarellano
#       Angélica Alemán
#       Damián Albino
#       Maximiliano Villegas
#       Jacqueline Ojeda
#
#   Recursos utilizados:
#       Anteojos y detección de bordes
#           Video de youtube.
#           https://www.youtube.com/watch?v=hcyAlrMEMec&list=WL
#
#           Código fuente.
#           https://github.com/savagecarol/snapchat_opencv
#
#       Conjunción de imágen en video
#           Tutoriales de OpenCV
#           https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_core/py_image_arithmetics/py_image_arithmetics.html 
#
#           Video de adición de marca de agua a la imagen
#           https://www.youtube.com/watch?v=QjKmgdrNCP0&ab_channel=CodingEntrepreneurs
#
#           Código fuente de marca de agua en imagen.
#           https://github.com/codingforentrepreneurs/OpenCV-Python-Series/blob/master/src/watermark.py 
#
#        Filtro de imagen
#           https://learnopencv.com/photoshop-filters-in-opencv/
#
#       Reproductor de audios
#           Video de youtube.
#           https://www.youtube.com/watch?v=xn9egHOQ16k
#
#       Código muestra del profesor Rubén Álvarez de la actividad 5 de la semana Tec.
#           camera_python.py
#
#
##############################################################



def musica():
    """
        Esta función inicializa el mixer de la librería pygame
        para cargar una canción y reproducirla.
    """
    #   Se inicializa el mixer.
    mixer.init()
    #   Se define volumen y carga canción.
    mixer.music.load("Quieres_Ser_Mi_Novia.mp3")
    mixer.music.set_volume(0.1)

def transparenteOverlay(src, overlay , pos = (0,0)  , scale = 1):
    """
        numpy.ndarray   src         |   
        numpy.ndarray   overlay     |
        tuple           pos         |
        int             scale       |

        Esta función permite utilizar los anteojos solares.
    
    """

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



def redimension(imagen, ancho = None, alto = None, interpolacion = cv2.INTER_AREA):
    """
        string imagen     | Localización de la imagen a mostrar.
        None ancho        | Longitud horizontal de la imagen, se convierte en entero.
        None alto         | Longitud vertical de la imagen, se convierte en entero.
        cv2 interpolacion | Interpolacion bilineal con la imagen. Permanece default.

        Esta función recibe una imagen y un tamaño a a justar, posteriormente
        modifica el tamaño de la imagen a las dimensiones deseadas.
    
    """
    (y, x) = imagen.shape[:2] 
    dimension = None

    if ancho is None and alto is None:
        return imagen
    if ancho is None:
        r = alto /float(y)
        dimension = (int(x * r), alto)
    else:
        r = ancho /float(x)
        dimension = (x, int(y * r))

    return cv2.resize(imagen, dimension, interpolation = interpolacion)



#   Programa final
if __name__ == '__main__':
    musica()
    #   Lee una imagen
    imagen = cv2.imread('kieres.png', -1)
    parser = argparse.ArgumentParser(description='Camera visualization')

    #   Argumentos posicionales.
    parser.add_argument('-i', '--cameraSource', default=0, help="Introduce number or camera path, default is 0 (default cam)")

    
    args = vars(parser.parse_args())


    cap = cv2.VideoCapture(args["cameraSource"]) #0 local o primary camera

    # Método eficaz para la detección de objetos (cara)
    cascada = cv2.CascadeClassifier('face.xml') 
    # Lee la imagen de los lentes que se van a mostrar 
    lentes_var = cv2.imread("lentes.png" , -1) 

    #   Inicia a sonar la música
    mixer.music.play()
    
    #   Cambia el tamaño de la imagen.
    foto = redimension(imagen, alto = 230)

    #   Cambia la estructura de color la imagen 
    foto = cv2.cvtColor(foto, cv2.COLOR_BGR2BGRA)
    
    while cap.isOpened():
        #   Inicia la lectura de la cámara y se cambia el formato de color.
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        frame_h, frame_w, frame_c = frame.shape
        #   Cambia los 4 canales BGR y Alfa
        overlay = np.zeros((frame_h, frame_w, 4), dtype='uint8')

        foto_h, foto_w, foto_c = foto.shape
        # Posiciona la imagen en un punto de la videocamara.
        for i in range(0, foto_h):
            for j in range(0, foto_w):
                if foto[i, j][3] != 0:
                    overlay[70+i, 30+j] = foto[i, j]
                        
        #   Agrega la imagen con el video en vivo.
        cv2.addWeighted(overlay, .7, frame, .8, 0, frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        
        #   Sección de filtro de color
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            #convertimos la imagen a una matriz RGB
            frame = np.array(frame, dtype=np.float64)
            frame = cv2.transform(frame, np.matrix([[0.400, 0.130, 0.200],[0.100, 0.200, 0.130],[0.140, 0.180, 0.180]])) #seleccionamos los valores RGB para dar una tonalidad rojiza a la imagen
            frame[np.where(frame > 255)] = 255 # cualquier valor mayor a 255, igualarlo a 255
            frame = np.array(frame, dtype=np.uint8)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        

            
            gris = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # Convirtiendo de color a grises
            faces =cascada.detectMultiScale(gris ,1.3 , 5 , 0 , minSize=(120,120) , maxSize=(350,350)) 
        
        # Para detectar objetos de diferentes tamaños
        for (x,y,w,h) in faces:
            if h> 0 and w>0:
                    
                 # Tamaños para los lentes
                lentes_symin = int(y+ 1.5 * h/5)
                lentes_symax = int(y + 2.5 * h /5)
                sh_glass = lentes_symax - lentes_symin

                #   Posicionamiento de los anteojos de sol
                lentes_ori = frame [lentes_symin:lentes_symax, x:x+w]
                lentes_mostrar = cv2.resize(lentes_var, (w, sh_glass), interpolation= cv2.INTER_CUBIC)
                transparenteOverlay(lentes_ori, lentes_mostrar)

        if not ret:
            break
        if frame is None:
            break

        cv2.imshow("Video webcam", frame)

        #   Cierra la cámara al presionar la tecla ESC.
        k = cv2.waitKey(10)
        if k==27:
            #   La canción termina.
            mixer.music.stop()
            break

    #   Cierra las ventanas y termina el programa.
    cap.release()
    cv2.destroyAllWindows()

    #Hola


