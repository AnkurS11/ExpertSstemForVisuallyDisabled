import os
import boto3
import cv2
import pytesseract
from gtts import gTTS
from playsound import playsound
import matplotlib.pyplot as plt

# Connects pytesseract(wrapper) to the trained tesseract module
pytesseract.pytesseract.tesseract_cmd = "C:\Program Files (x86)\Tesseract-OCR\Tesseract.exe"

dict_images = { "C:/Users/ankur/Downloads/specialised_project/senthil.jpg" : "Professor Senthilnathan", "C:/Users/ankur/Downloads/specialised_project/thiru.jpg" : "Professor Thirunavukkarasu", "C:/Users/ankur/Downloads/specialised_project/Adarsh.jpg" : "Adarsh", "C:/Users/ankur/Downloads/Ankur/Ankur_Sharma.jpg" : "Ankur", "C:/Users/ankur/Downloads/specialised_project/Amber.jpg" : "Amber"}

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
    video = cv2.VideoCapture("https://192.168.137.230:8080/video")
    # Setting width and height for video feed
    video.set(3, 640)
    video.set(4, 480)

    # Capture one frame from the video feed
    extra, frames = video.read()
    data4 = pytesseract.image_to_data(frames)

    print("OK")
    cv2.waitKey(0)

    img = frames
    cv2.imwrite("filename.png", img)

    target_file = "C:/Users/ankur/Downloads/specialised_project/Real-time-OCR-Text-To-Speech-with-Tesseract-main/filename.png"

    name = ""

    for i in dict_images:
        source_file = i

        face_matches = compare_faces(source_file, target_file)
        #print("Face matches: " + str(face_matches))

        if face_matches == 1:
            name = dict_images[i]
            break

    if name == "":
        line = "Not a teacher at Christ"
        language = 'en'
        speech = gTTS(text=line, lang=language, slow=False)
        speech.save("test.mp3")
        playsound("test.mp3")
        return 0

    from PIL import Image

    input_image = Image.open(target_file)
    target_image = Image.open(i)

    #target_image.show()
    #input_image.show()

    plt.figure(figsize=(10, 10), constrained_layout=False)

    plt.subplot(121), plt.imshow(input_image)
    plt.title("Input Image", fontsize=10), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(target_image)
    plt.title("Target image", fontsize=10), plt.xticks([]), plt.yticks([])

    plt.show()

    cv2.waitKey(0)

    line = name + "from Department of Computer Science, Christ university"
    language = 'en'
    speech = gTTS(text=line, lang=language, slow=False)
    speech.save("test.mp3")

    playsound("test.mp3")


if __name__ == "__main__":
    main()
