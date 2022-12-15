import os

import boto3
import cv2
import pytesseract
from gtts import gTTS
from playsound import playsound


# Connects pytesseract(wrapper) to the trained tesseract module
pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\Tesseract.exe"

dict_images = { "C:/Users/ankur/Downloads/Adarsh.jpg" : "Adarsh", "C:/Users/ankur/Downloads/Ankur_Sharma.jpg" : "Ankur", "C:/Users/ankur/Downloads/Amber.jpg" : "Amber"}

def compare_faces(sourceFile, targetFile):
    client = boto3.client('rekognition')

    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')

    response = client.compare_faces(SimilarityThreshold=80,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})

    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])
        print('The face at ' +
              str(position['Left']) + ' ' +
              str(position['Top']) +
              ' matches with ' + similarity + '% confidence')

    imageSource.close()
    imageTarget.close()
    return len(response['FaceMatches'])


def main():

    # Video feed
    video = cv2.VideoCapture("https://192.168.137.218:8080/video")
    # Setting width and height for video feed
    video.set(3, 640)
    video.set(4, 480)

    # Capture one frame from the video feed
    extra, frames = video.read()
    data4 = pytesseract.image_to_data(frames)

    img = frames
    cv2.imwrite("filename.png", img)

    target_file = "C:/Users/91911/PycharmProjects/FaceRecog/filename.png"
        
    for i in dict_images:
        source_file = i

        face_matches = compare_faces(source_file, target_file)
        #print("Face matches: " + str(face_matches))

        if face_matches == 1:
            name = dict_images[i]
            break

    import matplotlib.pyplot as plt
    f, ax = plt.subplots(1,2)

    ax[0].imshow('Image Input', frames) #first image
    ax[1].imshow('Image Trained', i) #second image
    plt.show()

    cv2.waitKey(0)
    
    line = "Ye to" + name + "hai"
    language = 'en'
    speech = gTTS(text=line, lang=language, slow=False)
    speech.save("test.mp3")

    playsound("test.mp3")


if __name__ == "__main__":
    main()
