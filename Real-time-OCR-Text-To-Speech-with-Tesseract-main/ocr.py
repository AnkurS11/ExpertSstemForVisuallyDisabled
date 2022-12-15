import cv2
import pytesseract
import base64


def img_to_speech(img_in_base64):
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files (x86)/Tesseract-OCR/Tesseract.exe"
    image_64_decode = base64.decodebytes(img_in_base64)
    image_result = open('target.jpg', 'wb')  # create a writable image and write the decoding result
    image_result.write(image_64_decode)

    final = cv2.imread('target.jpg')
    data4 = pytesseract.image_to_data(final)
    #print(data4.splitlines())
    str = ""
    for z, a in enumerate(data4.splitlines()):
        # Counter
        if z != 0:
            # Converts 'data1' string into a list stored in 'a'
            a = a.split()
            # Checking if array contains a word
            if len(a) == 12:
                # Storing values in the right variables
                x, y = int(a[6]), int(a[7])
                w, h = int(a[8]), int(a[9])
                # Display bounding box of each word
                cv2.rectangle(final, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # Display detected word under each bounding box
                cv2.putText(final, a[11], (x - 15, y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 1)
                str = str + a[11] + " "

    # Output the bounding box with the image
    cv2.imshow('Image output', final)
    cv2.waitKey(0)
    return str

image = open('C:/Users/ankur/Downloads/specialised_project/Real-time-OCR-Text-To-Speech-with-Tesseract-main/Capture_1.JPG', 'rb')
image_read = image.read()
image_64_encode = base64.b64encode(image_read)
print(image_64_encode)
speak = img_to_speech(image_64_encode)
print(speak)
