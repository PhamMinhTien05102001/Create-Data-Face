import os
import cv2
import dlib

detector = dlib.get_frontal_face_detector()

num_class = 0   #Minh 0, Quang 1, Thịnh 2, Tiến 3
path_folder = "Name"
path_image = os.path.join(path_folder, "images")
path_label = os.path.join(path_folder, "Label")

cap = cv2.VideoCapture(0)
index_image = 0
while True:
    _, frame = cap.read()
    print(index_image)
    #cv2.imshow("truoc", frame)

    frame = cv2.resize(frame, (640, 640))
    frame = cv2.GaussianBlur(frame, (3, 3), 0)
    frame = cv2.bilateralFilter(frame, 5, 20, 20)

    if not os.path.exists(path_folder):
        os.mkdir(path_folder)
        os.mkdir(path_image)
        os.mkdir(path_label)
    else:
        if not os.path.exists(path_label):
            os.mkdir(path_label)
        if not os.path.exists(path_image):
            os.mkdir(path_image)

    name = path_folder + "_" + str(index_image)
    name_image = name + ".jpg"
    name_label = name + ".txt"


    height, wight, _ = frame.shape
    label_format = ""
    faces = detector(frame)
    if faces:
        cv2.imwrite(os.path.join(path_image, name_image), frame)
        print("Face", faces)
        index_image += 1
        for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()
            cv2.rectangle(img=frame, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 0), thickness=4)

            x_center = (x1 + x2) / (2 * wight)
            y_center = (y1 + y2) / (2 * height)
            w = (x2 - x1) / wight
            h = (y2 - y1) / height

            label_format += str(num_class) + " " + str(x_center) + " " + str(y_center) + " " + str(w) + " " + str(h)

        new_label = open(os.path.join(path_label, name_label), 'w')
        new_label.write(label_format)
        if index_image % 200 == 0:
            break

    img_resize = cv2.resize(frame, (640, 640))
    cv2.imshow("anh", img_resize)

    k = cv2.waitKey(200)
    if k == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
