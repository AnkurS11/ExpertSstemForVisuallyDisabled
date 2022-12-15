import boto3


def detect_labels(photo):

    client = boto3.client('rekognition')

    response = client.detect_labels(Image={'Bytes': photo.read()}, MaxLabels=10)
    from PIL import Image

    input_image = Image.open(photo)

    print('Detected labels for ')
    input_image.show()
    print()
    for label in response['Labels']:
        print("Label: " + label['Name'])
        print("Confidence: " + str(label['Confidence']))
        print("Instances:")
        for instance in label['Instances']:
            print("  Bounding box")
            print("    Top: " + str(instance['BoundingBox']['Top']))
            print("    Left: " + str(instance['BoundingBox']['Left']))
            print("    Width: " + str(instance['BoundingBox']['Width']))
            print("    Height: " + str(instance['BoundingBox']['Height']))
            print("  Confidence: " + str(instance['Confidence']))
            print()

        print("Parents:")
        for parent in label['Parents']:
            print("   " + parent['Name'])
        print("----------")
        print()
    return len(response['Labels'])


def main():
    photo = open('Ankur_Sharma.jpg', 'rb')
    label_count = detect_labels(photo)
    print("Labels detected: " + str(label_count))


if __name__ == "__main__":
    main()

