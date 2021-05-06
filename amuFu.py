import numpy as np
import cv2

#https://github.com/codingforentrepreneurs/OpenCV-Python-Series/blob/master/src/watermark.py

cap = cv2.VideoCapture(0)

#   Se lee la imagen a mostrar
imagen = cv2.imread('kieres.png', -1)


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

#   Cambia el tamaño de la imagen.
img = redimension(imagen, alto = 230)

#   Cambia la estructura de color la imagen 
img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

while(True):
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    #   Cambia los 4 canales BGR y Alfa
    overlay = np.zeros((frame_h, frame_w, 4), dtype='uint8')

    watermark_h, watermark_w, watermark_c = watermark.shape
    # Posiciona la imagen en un punto de la videocamara.
    for i in range(0, watermark_h):
        for j in range(0, watermark_w):
            if watermark[i, j][3] != 0:
                overlay[70+i, 30+j] = watermark[i, j]
    #   Agrega la imagen con el video en vivo.
    cv2.addWeighted(overlay, .65, frame, .8, 0, frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    #   Muestra el resultado
    cv2.imshow('a', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

#   Cierra las ventanas.
cap.release()

cv2.destroyAllWindows()
