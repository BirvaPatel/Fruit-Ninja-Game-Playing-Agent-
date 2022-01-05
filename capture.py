import cv2
import imutils
import numpy as np
import os

# global variables
bg = None
image_x, image_y = 64, 64
#Ask for gesture name
ges_name = input("Enter gesture name: ")
#delete file directory if exists
if not os.path.exists('./mydata/training_set/' + ges_name):
        os.mkdir('./mydata/training_set/' + ges_name)
if not os.path.exists('./mydata/test_set/' + ges_name):
        os.mkdir('./mydata/test_set/' + ges_name)

test_set_image_name = 1
os.environ["CUDA_VISIBLE_DEVICES"]="1";

def calc_avg(image, avgwght):
    global bg

    if bg is None:
        bg = image.copy().astype("float")
        return

    cv2.accumulateWeighted(image, bg, avgwght)

def segment(image, threshold=25):
    global bg

    diff = cv2.absdiff(bg.astype("uint8"), image)

    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    ( cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) == 0:
        return
    else:
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)

if __name__ == "__main__":
 
    avgwght = 0.5

    cam = cv2.VideoCapture(0)

    tp, rt, bt, lt = 10, 350, 225, 590

    num_frames = 0

    while(True):

        (grabbed, frame) = cam.read()

        frame = imutils.resize(frame, width=700)

        frame = cv2.flip(frame, 1)

        clone = frame.copy()

        (height, width) = frame.shape[:2]

        roi = frame[tp:bt, rt:lt]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        if num_frames < 30:
            calc_avg(gray, avgwght)
        else:
            hand = segment(gray)

            if hand is not None:

                (thresholded, segmented) = hand

                cv2.drawContours(clone, [segmented + (rt, tp)], -1, (0, 0, 255))
                cv2.imshow("Thesholded", thresholded)
                save_img = cv2.resize(thresholded, (image_x, image_y))
               
                img_name = "./mydata/training_set/" + str(ges_name) + "/{}.png".format(test_set_image_name)
                cv2.imwrite(img_name, save_img)
                print("{} written!".format(img_name))
                test_set_image_name += 1
                if test_set_image_name == 1749:
                    break
                img_name = "./mydata/test_set/" + str(ges_name) + "/{}.png".format(test_set_image_name)
                cv2.imwrite(img_name, save_img)

        cv2.rectangle(clone, (lt, tp), (rt, bt), (0,255,0), 2)

        num_frames += 1

        cv2.imshow("Video", clone)

        keypress = cv2.waitKey(1) & 0xFF

        if keypress == ord("q"):
            break

cam.release()
cv2.destroyAllWindows()