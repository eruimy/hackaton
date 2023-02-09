import cv2
import pytesseract
import numpy as np

def get_text_image(image_link):

    image = cv2.imread(image_link)


    # threshold the image using Otsu's thresholding method
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(15,15))
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    cl = clahe.apply(l_channel)
    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl,a,b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    text = pytesseract.image_to_string(enhanced_img)
    return text