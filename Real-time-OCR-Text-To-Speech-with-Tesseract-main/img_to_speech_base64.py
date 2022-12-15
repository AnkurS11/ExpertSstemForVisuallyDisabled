import cv2
import pytesseract
# import base64
# from gtts import gTTS
# from playsound import playsound

def img_to_speech(img):
    pytesseract.pytesseract.tesseract_cmd = "C:\Program Files (x86)\Tesseract-OCR\Tesseract.exe"

    image_result = open('target.jpg', 'wb')  # create a writable image and write the decoding result
    image_result.write(img)

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
    # show_width, show_height = 1500, 1000
    cv2.imshow('Image output', final)
    cv2.waitKey(0)

    return str

image = open('para2.jpg', 'rb')
image_read = image.read()

speak = img_to_speech(image_read)
print(speak)
# language = 'en'
# speech = gTTS(text=speak, lang=language, slow=False)
# speech.save("test.mp3")
#
# playsound("test.mp3")
