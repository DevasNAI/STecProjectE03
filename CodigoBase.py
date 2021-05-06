import cv2
import time
import argparse
import numpy as np


if __name__ == '__main__':
    tiempoInicio = time.time()

    parser = argparse.ArgumentParser(description='Camera visualization')

    ### Positional arguments
    parser.add_argument('-i', '--cameraSource', default=0, help="Introduce number or camera path, default is 0 (default cam)")

    
    args = vars(parser.parse_args())


    cap = cv2.VideoCapture(args["cameraSource"]) #0 local o primary camera
    while cap.isOpened():
        
        #BGR image feed from camera
        success,img = cap.read()   
        img = cv2.cvtColor(res, cv2.COLOR_BGR2RGB) 
        
        #convertimos la imagen a una matriz RGB
        img = np.array(img, dtype=np.float64)
        img = cv2.transform(img, np.matrix([[0.400, 0.130, 0.200],[0.100, 0.200, 0.130],[0.140, 0.180, 0.180]])) #seleccionamos los valores RGB para dar una tonalidad rojiza a la imagen
        img[np.where(img > 255)] = 255 # cualquier valor mayor a 255, igualarlo a 255
        img = np.array(img, dtype=np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
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



