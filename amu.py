import numpy as np
import cv2


cap = cv2.VideoCapture(0)


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image
    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)
    # return the resized image
    return resized


save_path = 'saved-media/watermark.mp4'
frames_per_seconds = 24
#config = CFEVideoConf(cap, filepath=save_path, res='360p')

logo = cv2.imread('kieres.png', -1)
watermark = image_resize(logo, height=230)
watermark = cv2.cvtColor(watermark, cv2.COLOR_BGR2BGRA)

while(True):
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    frame_h, frame_w, frame_c = frame.shape
    overlay = np.zeros((frame_h, frame_w, 4), dtype='uint8')

    watermark_h, watermark_w, watermark_c = watermark.shape
    # replace overlay pixels with watermark pixel values

    for i in range(0, watermark_h):
        for j in range(0, watermark_w):
            if watermark[i, j][3] != 0:
                overlay[70+i, 30+j] = watermark[i, j]

    cv2.addWeighted(overlay, .65, frame, .8, 0, frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    
    cv2.imshow('a', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
