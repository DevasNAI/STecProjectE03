import cv2
import time
import argparse
from pygame import mixer

#Song load and volume settings
mixer.init()
mixer.music.load("Quieres_Ser_Mi_Novia.mp3")
mixer.music.set_volume(0.7)

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



