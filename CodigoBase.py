import cv2
import time
import argparse

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
    tiempoInicio = time.time()

    parser = argparse.ArgumentParser(description='Camera visualization')

    ### Positional arguments
    parser.add_argument('-i', '--cameraSource', default=0, help="Introduce number or camera path, default is 0 (default cam)")

    
    args = vars(parser.parse_args())


    cap = cv2.VideoCapture(args["cameraSource"]) #0 local o primary camera
    cascada = cv2.CascadeClassifier('face.xml') # método eficaz para la detección de objetos (cara)
    lentes_var = cv2.imread("lentes.png" , -1) # leer la imagen de los lentes que se van a mostrar 

    while cap.isOpened():
        
        #BGR image feed from camera
        success,img = cap.read()    
        if success:
            gris = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # convirtiendo de color a grises
            faces =cascada.detectMultiScale(gris ,1.3 , 5 , 0 , minSize=(120,120) , maxSize=(350,350)) 
            # para detectar objetos de diferentes tamaños

            for (x,y,w,h) in faces:
            if h> 0 and w>0:
                # tamaños para los lentes
                lentes_symin = int(y+ 1.5 * h/5)
                lentes_symax = int(y + 2.5 * h /5)
                sh_glass = lentes_symax - lentes_symin

        if not success:
            break
        if img is None:
            break

        
        cv2.imshow("Video webcam", img)

        k = cv2.waitKey(10)
        if k==27:
            break


    cap.release()
    cv2.destroyAllWindows()


    print('Script took %f seconds.' % (time.time() - tiempoInicio))



